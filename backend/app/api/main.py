from fastapi import APIRouter

from app.api.routes import cars, login, users, utils

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(cars.router)
