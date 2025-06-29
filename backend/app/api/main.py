from fastapi import APIRouter

from app.api.routes import cars, codrives, login, rides, users, utils

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(cars.router)
api_router.include_router(rides.router)
api_router.include_router(codrives.router)
