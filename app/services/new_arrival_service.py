from fastapi import Depends

from app.repositories import NewArrivalRepository, NewArrivalDetailRepository


class NewArrivalService:

    def __init__(
            self,
            new_arr_repository: NewArrivalRepository = Depends(),
            new_arr_det_repository: NewArrivalDetailRepository = Depends()
    ):
        self.new_arr_repository = new_arr_repository
        self.new_arr_det_repository = new_arr_det_repository

    async def get_arrivals(self) -> list:
        pass

    async def get_arr_details_by_arrive_id(self) -> list:
        pass

    async def create_new_arrive(self):
        pass

    async def add_new_arr_detail(self):
        pass

    async def update_arrive(self):
        pass

    async def update_arr_detail(self):
        pass

    async def delete_arrive(self):
        pass

    async def delete_arr_detail(self):
        pass

    async def transfer_arrive_to_warehouse(self):
        pass

    async def cancel_transfer_arrive_to_warehouse(self):
        pass
