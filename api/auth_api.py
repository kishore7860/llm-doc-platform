from fastapi import APIRouter
from fastapi_jwt_auth import AuthJWT

auth_router = APIRouter()

@auth_router.post("/login")
def login(username: str, password: str, Authorize: AuthJWT = Depends()):
    # Fake user, replace with DB lookup + hash check
    if username == "admin" and password == "admin":
        access_token = Authorize.create_access_token(subject=username, user_claims={"role": "admin"})
        return {"access_token": access_token}
    raise HTTPException(status_code=401, detail="Invalid credentials")