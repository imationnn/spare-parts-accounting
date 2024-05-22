from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import PhysicalClient, JuridicalClient
from app.repositories import BaseRepository


class PhysicalClientRepository(BaseRepository):
    model = PhysicalClient


class JuridicalClientRepository(BaseRepository):
    model = JuridicalClient
