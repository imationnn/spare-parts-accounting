from app.models import Brand
from app.repositories import BaseRepository


class BrandRepository(BaseRepository):
    model = Brand
