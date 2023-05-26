from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse
from app.schemas.default_schemas import DefaultResponse
from app.schemas.user import (
    CreateUserDetail,
    RequestRegister,
    ResponseRegister,
    RequestLogin,
    ResponseLogin,
    UpdateProfile,
    UpdatePassword,
    GetLeaderboard,
    GetUserData
)
from firebase_admin import auth
from app.deps.firebase import db
from datetime import date, datetime

router = APIRouter()

@router.post("/register", response_model=ResponseRegister, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: RequestRegister
) -> JSONResponse:
    if request.password != request.confirmPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and Confirm Password are not the same",
        )
    try:
        user = auth.create_user(email=request.email, display_name=request.username, password=request.password)
        try:
            doc_ref = db.collection('users').document(user.uid)
            doc_ref.set({
                'id': user.uid,
                'email': user.email,
                'username': user.display_name,
                'password': request.password,
            })
            return ResponseRegister(
                message="Register success",
                data=GetUserData(
                    user_id=user.uid,
                    username=user.display_name,
                    email=user.email
                )
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists, please do login instead",
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=ResponseLogin, status_code=status.HTTP_200_OK)
async def login_user(
    request: RequestLogin
) -> JSONResponse:
    try:
        user = auth.get_user_by_email(request.email)
        try:
            doc_ref = db.collection('users').document(user.uid)
            doc_snapshot = doc_ref.get()
            if doc_snapshot.exists:
                data = doc_snapshot.to_dict()
                if data.get('password') != request.password:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Password is incorrect",
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User not found",
                )

            return ResponseLogin(
                message="Login success",
                data=GetUserData(
                    user_id=user.uid,
                    username=user.display_name,
                    email=user.email
                )
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
    
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/userDetail", status_code=status.HTTP_200_OK)
async def create_user_detail(
    request: CreateUserDetail,
    user_uid: str = Header(None)
    # user_id: str = Depends(authenticate_user)
) -> JSONResponse:

    try:
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()
        if doc_snapshot.exists:
            data = doc_snapshot.to_dict()
            name = request.name or data.get('name')
            contactNumber = request.contactNumber or data.get('contactNumber')
            dateOfBirth = request.dateOfBirth or datetime.fromtimestamp(data.get('dateOfBirth'))
            gender = request.gender or data.get('gender')
            height = request.height or data.get('height')
            weight = request.weight or data.get('weight')
            target = request.target or data.get('target')
            weightTarget = request.weightTarget or data.get('weightTarget')

            # Calculate age based on date of birth
            today = date.today()
            age = request.age or (today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day)))

            # Calculate BMR based on gender, weight, height, and age
            if gender.lower() == "male":
                bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
            elif gender.lower() == "female":
                bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)

            # Calculate calorie needs, water needs, and sleep needs
            calorieNeeds = int(bmr * 1.2)
            waterNeeds = weight * 0.033
            sleepNeeds = 8
            try:
                doc_ref.update({
                    'username': name,
                    'contactNumber': contactNumber,
                    'dateOfBirth': datetime.combine(dateOfBirth, datetime.min.time()).timestamp(),
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
                return DefaultResponse(
                    message="User detail created",
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e),
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


    # email = request.email

    # userFound = []
    # user = {}
    # docId = ""
    # docs = db.collection('user').where('email', '==', email).stream()
    # for doc in docs:
    #     userFound.append(doc.to_dict())
    #     docId = doc.id
    
    # if len(userFound) > 1:
    #     raise HTTPException(status_code=400, detail="Multiple users with same email")
    # if len(userFound) == 0:
    #     raise HTTPException(status_code=400, detail="No user with this email")
    
    # user =  userFound[0]
    # print(user) 
    # id = str(request.id)
    # name = request.name
    # imgUrl = request.imgUrl
    # contactNumber = request.contactNumber
    # dateOfBirth = request.dateOfBirth
    # dt_with_time = datetime.combine(dateOfBirth, datetime.min.time()).timestamp()

    # print(dateOfBirth)

    # today = date.today()
    # age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
    # print(age)

    # gender = request.gender
    # height = request.height
    # weight = request.weight
    # target = request.target
    # weightTarget = request.weightTarget

    # if gender.lower() == "male":
    #     bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
    # elif gender.lower() == "female":
    #     bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
    # # else:
    # #     raise ValueError('Invalid gender. Please enter female or male')

    # calorieNeeds = (int(bmr * 1.2))
    # # assuming sedentary lifestyle
    # waterNeeds = weight * 0.033
    # # assuming 33ml per kg of body weight
    # sleepNeeds = 8
    # # assuming 8 hours of sleep per day

    # db.collection('user').document(docId).update({
    #     'id': id,
    #     'name': name,
    #     'imgUrl': imgUrl,
    #     'contactNumber': contactNumber,
    #     'dateOfBirth': dt_with_time,
    #     'age': age,
    #     'gender' : gender,
    #     'height': height,
    #     'weight': weight,
    #     'target': target,
    #     'weightTarget': weightTarget,
    #     'calorieNeeds': calorieNeeds,
    #     'waterNeeds': waterNeeds,
    #     'sleepNeeds': sleepNeeds
    # })

    
    # return {"id": id
    #         ,"name": name
    #         ,"imgUrl": imgUrl
    #         ,"contactNumber": contactNumber
    #         ,"dateOfBirth": dateOfBirth
    #         , "gender": gender
    #         , "height": height
    #         , "weight": weight
    #         , "target": target
    #         , "weightTarget": weightTarget
    #         , "calorieNeeds": calorieNeeds
    #         , "waterNeeds": waterNeeds
    #         , "sleepNeeds": sleepNeeds
    #         }

    # return {"message": "This is the user detail post endpoint"}
    
    
   
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