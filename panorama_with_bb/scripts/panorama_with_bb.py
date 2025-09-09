import argparse
import requests
import math
import os
import logging
from typing import List, Dict, Tuple, Optional, Set
from urllib.parse import urlencode
from datetime import datetime
from requests.exceptions import HTTPError, SSLError
from PIL import Image, ImageDraw

# ----------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def feet_to_meters(feet: float) -> float:
    return feet * 0.3048


def bbox_from_circle(lat: float, lon: float, radius_m: float) -> Tuple[float, float, float, float]:
    """
    Approximate a bounding box around (lat, lon) with radius in meters.
    Returns (min_lat, max_lat, min_lon, max_lon).
    """
    delta_lat = radius_m / 111320
    delta_lon = radius_m / (111320 * math.cos(math.radians(lat)))
    return (lat - delta_lat, lat + delta_lat, lon - delta_lon, lon + delta_lon)


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate bearing in degrees from (lat1, lon1) to (lat2, lon2).
    """
    dLon = math.radians(lon2 - lon1)
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    y = math.sin(dLon) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dLon)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

# ----------------------------------------------------------------------------
# Fetch functions (return list of dicts with id, url, date, heading)
# ----------------------------------------------------------------------------

def fetch_flickr(lat: float, lon: float, radius_ft: float, api_key: str) -> List[Dict]:
    radius_km = feet_to_meters(radius_ft) / 1000
    params = {
        "method": "flickr.photos.search",
        "api_key": api_key,
        "lat": lat,
        "lon": lon,
        "radius": radius_km,
        "radius_units": "km",
        "extras": "geo,url_o,date_taken",
        "format": "json",
        "nojsoncallback": 1
    }
    resp = requests.get("https://api.flickr.com/services/rest/", params=params, verify=False)
    resp.raise_for_status()
    photos = resp.json().get("photos", {}).get("photo", [])
    results = []
    for p in photos:
        url = p.get("url_o") or p.get("url_m")
        if not url:
            continue
        dt = p.get("datetaken", "")
        date_str = dt.split(" ")[0].replace("-", "") if dt else "nodate"
        results.append({"id": p["id"], "url": url, "date": date_str, "heading": "noaz"})
    return results


def fetch_wikimedia(lat: float, lon: float, radius_ft: float) -> List[Dict]:
    raw_m = feet_to_meters(radius_ft)
    radius_m = max(10, min(int(raw_m), 10000))
    base = "https://commons.wikimedia.org/w/api.php"
    gs_params = {
        "action": "query", "format": "json", "list": "geosearch",
        "gscoord": f"{lat}|{lon}", "gsradius": radius_m,
        "gslimit": 50, "gsnamespace": 6, "formatversion": 2
    }
    r = requests.get(base, params=gs_params, verify=False); r.raise_for_status()
    data = r.json()
    if data.get("error"): raise RuntimeError(data["error"]["info"])
    pages = data.get("query", {}).get("geosearch", [])
    if not pages: return []
    page_ids = ",".join(str(p["pageid"]) for p in pages)
    ii_params = {"action":"query","format":"json","pageids":page_ids,
                 "prop":"imageinfo","iiprop":"url|timestamp","formatversion":2}
    r2 = requests.get(base, params=ii_params, verify=False); r2.raise_for_status()
    info = r2.json()
    results = []
    for pg in info.get("query", {}).get("pages", []):
        if "imageinfo" not in pg: continue
        ii = pg["imageinfo"][0]
        url = ii.get("url")
        ts = ii.get("timestamp", "")
        date_str = ts.split("T")[0].replace("-", "") if ts else "nodate"
        results.append({"id": pg["title"].replace("File:", "").replace("/", "_"),
                        "url": url, "date": date_str, "heading": "noaz"})
    return results


def fetch_google_streetview(lat: float, lon: float, api_key: str) -> List[Dict]:
    base = "https://maps.googleapis.com/maps/api/streetview"
    results = []
    for heading in range(0, 360, 60):
        params = {"size": "640x640", "location": f"{lat},{lon}",
                  "fov": 90, "heading": heading, "pitch": 0, "key": api_key}
        results.append({"id": f"gsv_{heading}", "url": f"{base}?{urlencode(params)}",
                        "date": "nodate", "heading": f"{heading:03d}"})
    return results

# ----------------------------------------------------------------------------
# Mapillary: fetch and download filtered by view and years
# ----------------------------------------------------------------------------

def fetch_mapillary_full(
    lat: float, lon: float, radius_ft: float, token: str,
    save_dir: str, years: Optional[Set[str]] = None, fov_deg: float = 90.0
) -> List[str]:
    """
    Fetch and download Mapillary images whose frame views the target point,
    optionally filtering by capture year set. Draw red overlay at target.
    """
    min_radius_m = max(20, feet_to_meters(radius_ft))
    min_lat, max_lat, min_lon, max_lon = bbox_from_circle(lat, lon, min_radius_m)
    bbox = f"{min_lon},{min_lat},{max_lon},{max_lat}"
    endpoint = "https://graph.mapillary.com/images"
    headers = {"Authorization": f"OAuth {token}"}
    params = {"bbox": bbox,
              "fields": "id,thumb_original_url,captured_at,compass_angle,computed_compass_angle,computed_geometry",
              "limit": 1000}
    try:
        resp = requests.get(endpoint, params=params, headers=headers, verify=False)
        resp.raise_for_status()
        items = resp.json().get("data", [])
    except (HTTPError, SSLError) as e:
        logging.error(f"[mapillary] Request error: {e}")
        return []
    except Exception as e:
        logging.error(f"[mapillary] Unexpected error: {e}")
        return []

    out_dir = os.path.join(save_dir, "mapillary")
    os.makedirs(out_dir, exist_ok=True)
    half_fov = fov_deg / 2.0
    saved_paths = []

    for img in items:
        # parse date and filter by years
        ts = img.get("captured_at")
        try:
            date_str = datetime.utcfromtimestamp(int(ts)/1000).strftime("%Y%m%d")
        except:
            date_str = "nodate"
        year = date_str[:4]
        if years and year not in years:
            continue
        # compute camera position and filter by FOV
        coords = img.get("computed_geometry", {}).get("coordinates")
        if not coords:
            continue
        cam_lon, cam_lat = coords
        target_bearing = calculate_bearing(cam_lat, cam_lon, lat, lon)
        exif = img.get("compass_angle")
        comp = img.get("computed_compass_angle")
        cam_heading = exif if exif is not None else comp
        if cam_heading is None:
            continue
        diff = abs((cam_heading - target_bearing + 180) % 360 - 180)
        if diff > half_fov:
            continue

        img_id = img.get("id")
        full_url = img.get("thumb_original_url")
        if not img_id or not full_url:
            continue
        heading_str = f"{int(cam_heading):03d}"

        # download image
        try:
            dl = requests.get(full_url, stream=True, verify=False)
            dl.raise_for_status()
            image = Image.open(dl.raw).convert("RGB")
        except Exception as e:
            logging.error(f"[mapillary] download failed: {e}")
            continue

        # overlay box
        width, height = image.size
        rel = (target_bearing - cam_heading + 360) % 360
        if rel > 180:
            rel -= 360
        x_px = int((rel/fov_deg + 0.5) * width)
        draw = ImageDraw.Draw(image)
        box_w = int(width * 0.02)
        draw.rectangle([(x_px-box_w, 0), (x_px+box_w, height)], outline="red", width=3)

        # save filtered
        filename = f"{img_id}_{date_str}_{heading_str}.jpg"
        path = os.path.join(out_dir, filename)
        try:
            image.save(path)
            logging.info(f"Saved [mapillary] → {path}")
            saved_paths.append(path)
        except Exception as e:
            logging.error(f"[mapillary] write error {path}: {e}")

    return saved_paths

# ----------------------------------------------------------------------------
# Download images utility
# ----------------------------------------------------------------------------

def download_images(services: Dict[str, List[Dict]], base_dir: str, years: Optional[Set[str]] = None):
    """
    Download images for services besides Mapillary, filtering by years if provided.
    """
    for svc, imgs in services.items():
        svc_dir = os.path.join(base_dir, svc)
        os.makedirs(svc_dir, exist_ok=True)
        if not imgs:
            logging.warning(f"No images for {svc}")
            continue
        for img in imgs:
            date_str = img.get("date", "nodate")
            year = date_str[:4]
            if years and year not in years:
                continue
            url = img.get("url") or img.get("thumb_original_url")
            if not url:
                continue
            try:
                resp = requests.get(url, stream=True, verify=False)
                resp.raise_for_status()
            except SSLError as e:
                logging.error(f"SSL error downloading {url}: {e}")
                continue
            ext = resp.headers.get("Content-Type", "image/jpeg").split("/")[-1]
            filename = f"{img.get('id')}_{date_str}_{img.get('heading','noaz')}.{ext}"
            path = os.path.join(svc_dir, filename)
            with open(path, 'wb') as f:
                for c in resp.iter_content(1024):
                    f.write(c)
            logging.info(f"Saved [{svc}] → {path}")

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser("Pull & download geotagged images")
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--radius", type=float, required=True, help="feet")
    parser.add_argument("--years", type=str, default=None,
                        help="Comma-separated list of years to include, e.g. '2021,2023'")
    parser.add_argument("--flickr_key", default=None)
    parser.add_argument("--wikimedia", action="store_true")
    parser.add_argument("--mapillary_token", default=None)
    parser.add_argument("--google_key", default=None)
    parser.add_argument("--azure_key", default=None)
    args = parser.parse_args()

    # parse years
    years = set(y.strip() for y in args.years.split(',')) if args.years else None

    # build base_dir
    r_m = feet_to_meters(args.radius)
    min_lat, max_lat, min_lon, max_lon = bbox_from_circle(args.lat, args.lon, r_m)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    base_dir = f"{ts}_{min_lat:.4f}_{min_lon:.4f}_{max_lat:.4f}_{max_lon:.4f}"
    os.makedirs(base_dir, exist_ok=True)
    logging.info(f"Saving images under {base_dir}/<service>/")

    # fetch non-Mapillary services
    services, errors = {}, {}
    if args.flickr_key:
        try:
            services["flickr"] = fetch_flickr(args.lat, args.lon, args.radius, args.flickr_key)
        except Exception as e:
            errors["flickr"] = str(e)
    if args.wikimedia:
        try:
            services["wikimedia"] = fetch_wikimedia(args.lat, args.lon, args.radius)
        except Exception as e:
            errors["wikimedia"] = str(e)
    if args.google_key:
        try:
            services["google"] = fetch_google_streetview(args.lat, args.lon, args.google_key)
        except Exception as e:
            errors["google"] = str(e)

    # download non-Mapillary
    download_images(services, base_dir, years)

    # Mapillary
    if args.mapillary_token:
        paths = fetch_mapillary_full(
            args.lat, args.lon, args.radius,
            args.mapillary_token, base_dir, years=years
        )
        for p in paths:
            logging.info(f"[mapillary] saved → {p}")

    # report errors
    for svc, msg in errors.items():
        logging.error(f"[{svc}] {msg}")

if __name__ == '__main__':
    main()

