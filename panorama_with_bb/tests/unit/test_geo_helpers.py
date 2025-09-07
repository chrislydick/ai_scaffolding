import importlib.util
from pathlib import Path


def load_script_module():
    path = Path(__file__).resolve().parents[2] / "scripts" / "panorama_with_bb.py"
    spec = importlib.util.spec_from_file_location("panorama_with_bb", str(path))
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_feet_to_meters_and_bbox_and_bearing():
    mod = load_script_module()
    assert abs(mod.feet_to_meters(10) - 3.048) < 1e-6
    # Rough bbox size for ~1000m radius at 47N
    min_lat, max_lat, min_lon, max_lon = mod.bbox_from_circle(47.0, -122.0, 1000.0)
    assert max_lat > min_lat and max_lon > min_lon
    # Bearing north should be ~0
    b = mod.calculate_bearing(47.0, -122.0, 48.0, -122.0)
    assert abs(b - 0.0) < 1.0

