from pathlib import Path
import subprocess
import sys


def test_build_web_generates_html(tmp_path: Path):
    out = tmp_path / "double-bubble-analyzer-multi.html"
    subprocess.check_call([sys.executable, "scripts/build_web.py", "--out", str(out)], cwd=str(Path(__file__).resolve().parents[2]))
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "PSE Double Bubble Analyzer — Multi" in text

