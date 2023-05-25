from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.default_model   import DefaultResponse
from app.schemas.user import (
    CreateUserDetail,
    Register,
    Login,
    UpdateProfile,
    UpdatePassword,
    GetLeaderboard
)
from firebase_admin import auth
from app.deps.auth import authenticate_user

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: Register
) -> JSONResponse:
    user = auth.create_user(email=request.email, password=request.password)
    return DefaultResponse(message="This is the register post endpoint")

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    request: Login
) -> JSONResponse:
    user = auth.get_user_by_email(request.email)
    return DefaultResponse(message=f'This is the login post endpoint with {user.uid}')

@router.post("/user/{user_id}/detail", status_code=status.HTTP_201_CREATED)
async def create_user_detail(
    request: CreateUserDetail
    # user_id: str = Depends(authenticate_user)
) -> JSONResponse:
    return DefaultResponse(message="This is the user detail post endpoint")
#! after POST user detail, create user statistic (actualNeed)

@router.put("/profile/{user_id}", status_code=status.HTTP_200_OK)
async def update_profile(
    profile_id: str,
    request: UpdateProfile
    # user_id: str = Depends(authenticate_user)
) -> JSONResponse:
    return DefaultResponse(message="This is the profile put endpoint")
#! after PUT Profile, update user statistic (actualNeed)

@router.put("/profile/{profile_id}/password", status_code=status.HTTP_200_OK)
async def update_password(
    profile_id: str,
    request: UpdatePassword
    # user_id: str = Depends(authenticate_user)
) -> JSONResponse:
    return {"message": "This is the profile password put endpoint"}

@router.get("/leaderboard", response_model=GetLeaderboard, status_code=status.HTTP_200_OK)
async def get_leaderboard():
    return DefaultResponse(message="This is the leaderboard get endpoint")