from app.models import MarginCategory
from app.repositories import BaseRepository


class MarginRepository(BaseRepository):
    model = MarginCategory
