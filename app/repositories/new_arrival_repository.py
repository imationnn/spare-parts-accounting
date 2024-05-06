from app.repositories import BaseRepository
from app.models import NewArrival, NewArrivalDetail


class NewArrivalRepository(BaseRepository):
    model = NewArrival


class NewArrivalDetailRepository(BaseRepository):
    model = NewArrivalDetail
