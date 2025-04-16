from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from datetime import timedelta


class Settings(BaseModel):
    authjwt_secret_key: str = "super-secret-key"
    authjwt_access_token_expires: timedelta = timedelta(minutes=60)  

@AuthJWT.load_config
def get_config():
    return Settings()

