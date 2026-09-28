"""Application services for uploaded media; media has no database table."""

from io import BytesIO
from uuid import uuid4

from fastapi import HTTPException
from PIL import Image, UnidentifiedImageError


class ImageUploadService:
    max_bytes = 5 * 1024 * 1024
    max_pixels = 25_000_000

    def __init__(self, uploads_dir):
        self.uploads_dir = uploads_dir

    def save(self, upload):
        data = upload.file.read(self.max_bytes + 1)
        if len(data) > self.max_bytes:
            raise HTTPException(413, "Image must be smaller than 5 MB.")
        try:
            with Image.open(BytesIO(data)) as image:
                if image.width * image.height > self.max_pixels:
                    raise HTTPException(413, "Image dimensions are too large.")
                image.load()
                name = f"{uuid4().hex}.webp"
                image.convert("RGB").save(self.uploads_dir / name, "WEBP")
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
            raise HTTPException(400, "Upload a valid image.") from error
        return {"url": f"/static/uploads/{name}"}
