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
    GetUserData,
    CheckUsername
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
                    'registeredAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
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


@router.post("/user/{user_uid}/detail", status_code=status.HTTP_200_OK)
async def create_user_detail(
    request: CreateUserDetail,
    user_uid: str
    # user_id: str = Depends(authenticate_user)
) -> JSONResponse:
    try:
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()

        # if user exists in firebase auth, but not exists in firestore
        if not doc_snapshot.exists:
            # get user data from firebase auth
            try:
                user = auth.get_user(user_uid)
                doc_ref.set({
                    'id': user.uid,
                    'email': user.email,
                    'username': user.display_name,
                        'registeredAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                })
                doc_ref = db.collection('users').document(user_uid)
                doc_snapshot = doc_ref.get()

            except auth.UserNotFoundError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User not found",
                )

        data = doc_snapshot.to_dict()
        username = request.username or data.get('username')
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
                'username': username,
                'name': name,
                'imgUrl': '',
                'contactNumber': contactNumber,
                'dateOfBirth': datetime.combine(dateOfBirth, datetime.min.time()).timestamp(),
                'age': age,
                'gender' : gender,
                'height': height,
                'weight': weight,
                'target': target,
                'weightTarget': weightTarget,
                'actualCalorie': 0,
                'actualWater': 0,
                'actualSleep': 0,
                'calorieNeeds': calorieNeeds,
                'waterNeeds': waterNeeds,
                'sleepNeeds': sleepNeeds,
                'points': 0,
                'emotionHistory': [],
            })
            return DefaultResponse(
                message="User detail created",
                data=data
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
   
@router.put("/user/{user_uid}/edit", status_code=status.HTTP_200_OK)
async def update_profile(
    request: UpdateProfile,
    user_uid: str
) -> JSONResponse:
    try:
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()
        if not doc_snapshot.exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )
        data = doc_snapshot.to_dict()
        name = request.name or data.get('name')
        imgUrl = request.imgUrl or data.get('imgUrl')
        contactNumber = request.contactNumber or data.get('contactNumber')

        dateOfBirth = request.dateOfBirth or datetime.fromtimestamp(data.get('dateOfBirth'))

        # Recalculate age based on date of birth
        today = date.today()
        age = (today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day)))

        # Recalculate BMR based on gender, weight, height, and age
        gender = data.get('gender')
        weight = data.get('weight')
        height = data.get('height')
        if gender.lower() == "male":
            bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
        elif gender.lower() == "female":
            bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)

        # Recalculate calorie needs, water needs, and sleep needs
        calorieNeeds = int(bmr * 1.2)
        waterNeeds = weight * 0.033
        sleepNeeds = 8

        
        try:
            updated_data = {
                'name': name,
                'contactNumber': contactNumber,
                'dateOfBirth': datetime.combine(dateOfBirth, datetime.min.time()).timestamp(),
                'age': age,
                'calorieNeeds': calorieNeeds,
                'waterNeeds': waterNeeds,
                'sleepNeeds': sleepNeeds
            }

            doc_ref.update(updated_data)
            return DefaultResponse(
                message="User profile updated",
                data=updated_data   
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.put("/user/{profile_id}/password", status_code=status.HTTP_200_OK)
async def update_password(
    profile_id: str,
    request: UpdatePassword
    # user_id: str = Depends(authenticate_user)
) -> JSONResponse:
    return {"message": "This is the profile password put endpoint"}

@router.get("/leaderboard", response_model=GetLeaderboard, status_code=status.HTTP_200_OK)
async def get_leaderboard() -> GetLeaderboard:
    try:
        users_ref = db.collection('users')
        query = users_ref.order_by('points')
        docs = query.stream()

        leaderboard = []

        for doc in docs:
            data = doc.to_dict()
            name = data.get('name')
            username = data.get('username')
            points = data.get('points')

            leaderboard.append({
                'name': name,
                'username': username,
                'points': points
            })
        
        return GetLeaderboard(
            message="Leaderboard retrieved",
            data=leaderboard
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get("/user/availability/{username}", response_model=CheckUsername, status_code=status.HTTP_200_OK)
async def check_username_availability(
    username: str
):
    try:
        users_ref = db.collection('users')
        query = users_ref.where('username', '==', username)
        docs = query.stream()

        if len(list(docs)) == 0:
            return CheckUsername(
                message="Username available",
                data=True
            )
        else:
            return CheckUsername(
                message="Username not available",
                data=False
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )