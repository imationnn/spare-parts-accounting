from contextlib import asynccontextmanager

import uvicorn
from app.api.routers import main_router
from fastapi import FastAPI

from app.config import settings


@asynccontextmanager
async def lifespan(_):
    from pre_start import main
    await main()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix=settings.api_v1_prefix)


if __name__ == '__main__':
    uvicorn.run('main:app')
