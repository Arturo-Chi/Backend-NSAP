from fastapi import FastAPI
from app.routes.clima import router as clima_router
from app.routes.weather_route import router as weather_router


app = FastAPI(title="API Nasa Space App Challenge")

app.include_router(weather_router)
