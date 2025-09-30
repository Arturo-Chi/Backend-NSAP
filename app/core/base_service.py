
class BaseService:
    def __init__(self, name: str):
        self.name = name

    def success(self, data: dict):
        return {
            "status": "success",
            "service": self.name,
            "data": data
        }

    def error(self, message: str):
        return{
            "status":"error",
            "service": self.name,
            "message": message
        }


    


