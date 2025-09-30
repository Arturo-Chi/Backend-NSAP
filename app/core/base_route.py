
from fastapi import APIRouter

class BaseRoute:
    def __init__(self, prefix: str, tag: str):
        self.router = APIRouter(prefix=prefix, tags = [tag])


    def get_router(self):
        return self.router