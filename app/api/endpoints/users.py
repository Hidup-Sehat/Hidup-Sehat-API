from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.user import (
    CreateUserDetail,
    Register,
    Login,
    UpdateProfile,
    UpdatePassword,
    GetLeaderboard
)
from ..firebase import db
from datetime import date, datetime

router = APIRouter()

@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(
    request: Register
) -> JSONResponse:
    return {"message": "This is the register post endpoint"}

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    request: Login
) -> JSONResponse:
    return {"message": "This is the login post endpoint"}

@router.post("/userDetail", status_code=status.HTTP_200_OK)
async def create_user_detail(
    request: CreateUserDetail
) -> JSONResponse:
    email = request.email

    userFound = []
    user = {}
    docId = ""
    docs = db.collection('user').where('email', '==', email).stream()
    for doc in docs:
        userFound.append(doc.to_dict())
        docId = doc.id
    
    if len(userFound) > 1:
        raise HTTPException(status_code=400, detail="Multiple users with same email")
    if len(userFound) == 0:
        raise HTTPException(status_code=400, detail="No user with this email")
    
    user =  userFound[0]
    print(user) 
    id = str(request.id)
    name = request.name
    imgUrl = request.imgUrl
    contactNumber = request.contactNumber
    dateOfBirth = request.dateOfBirth
    dt_with_time = datetime.combine(dateOfBirth, datetime.min.time()).timestamp()

    print(dateOfBirth)

    today = date.today()
    age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
    print(age)

    gender = request.gender
    height = request.height
    weight = request.weight
    target = request.target
    weightTarget = request.weightTarget

    if gender.lower() == "male":
        bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
    elif gender.lower() == "female":
        bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
    # else:
    #     raise ValueError('Invalid gender. Please enter female or male')

    calorieNeeds = (int(bmr * 1.2))
    # assuming sedentary lifestyle
    waterNeeds = weight * 0.033
    # assuming 33ml per kg of body weight
    sleepNeeds = 8
    # assuming 8 hours of sleep per day

    db.collection('user').document(docId).update({
        'id': id,
        'name': name,
        'imgUrl': imgUrl,
        'contactNumber': contactNumber,
        'dateOfBirth': dt_with_time,
        'age': age,
        'gender' : gender,
        'height': height,
        'weight': weight,
        'target': target,
        'weightTarget': weightTarget,
        'calorieNeeds': calorieNeeds,
        'waterNeeds': waterNeeds,
        'sleepNeeds': sleepNeeds
    })

    
    return {"id": id
            ,"name": name
            ,"imgUrl": imgUrl
            ,"contactNumber": contactNumber
            ,"dateOfBirth": dateOfBirth
            , "gender": gender
            , "height": height
            , "weight": weight
            , "target": target
            , "weightTarget": weightTarget
            , "calorieNeeds": calorieNeeds
            , "waterNeeds": waterNeeds
            , "sleepNeeds": sleepNeeds
            }
    # return {"message": "This is the user detail post endpoint"}
    
    
    
#! after POST user detail, create user statistic (actualNeed)

@router.put("/profile/{user_id}", status_code=status.HTTP_200_OK)
async def update_profile(
    profile_id: str,
    request: UpdateProfile
) -> JSONResponse:
    return {"message": "This is the profile put endpoint"}
#! after PUT Profile, update user statistic (actualNeed)

@router.put("/profile/{profile_id}/password", status_code=status.HTTP_200_OK)
async def update_password(
    profile_id: str,
    request: UpdatePassword
) -> JSONResponse:
    return {"message": "This is the profile password put endpoint"}

@router.get("/leaderboard", response_model=GetLeaderboard, status_code=status.HTTP_200_OK)
async def get_leaderboard():
    return {"message": "This is the leaderboard get endpoint"}