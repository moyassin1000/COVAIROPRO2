from pathlib import Path

from app.utils.file_utils import safe_output_path


def test_safe_output_path_avoids_overwrite(tmp_path):
    source = tmp_path / "sample.png"
    source.write_text("x")
    first = safe_output_path(source, tmp_path, "jpg")
    first.write_text("x")
    second = safe_output_path(source, tmp_path, "jpg")
    assert second.name == "sample_1.jpg"
