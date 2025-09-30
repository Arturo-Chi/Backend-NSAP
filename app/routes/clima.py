
from app.core.base_route import BaseRoute
from app.services.clima_service import ClimaService

clima_service = ClimaService()

base_route = BaseRoute(prefix="/clima", tag="Clima")
router = base_route.get_router()


@router.get("/")
def get_weatherParams(lat: float, lon:float, fecha: str):
    return clima_service.obtener_clima(lat, lon, fecha)
