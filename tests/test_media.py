from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile
from PIL import Image

from app.services.media import ImageUploadService


def image_upload() -> UploadFile:
    data = BytesIO()
    Image.new("RGB", (8, 8), (30, 90, 180)).save(data, "PNG")
    return UploadFile(file=BytesIO(data.getvalue()), filename="source.png")


def test_upload_image_is_saved_as_webp(tmp_path):
    uploads = tmp_path / "uploads"
    uploads.mkdir()

    result = ImageUploadService(uploads).save(image_upload())

    target = uploads / result["url"].rsplit("/", 1)[-1]
    assert target.is_file()
    with Image.open(target) as saved:
        assert saved.format == "WEBP"


def test_storage_failure_is_not_reported_as_an_invalid_image(tmp_path, monkeypatch):
    uploads = tmp_path / "uploads"
    uploads.mkdir()
    upload = image_upload()

    def fail_to_save(*_args, **_kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr(Image.Image, "save", fail_to_save)

    with pytest.raises(HTTPException) as error:
        ImageUploadService(uploads).save(upload)

    assert error.value.status_code == 500
    assert error.value.detail == "Unable to save image. Please try again later."
