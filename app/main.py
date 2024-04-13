import uvicorn
from app.api import main_router
from fastapi import FastAPI

from app.config import settings


app = FastAPI()
app.include_router(main_router, prefix=settings.api_v1_prefix)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
