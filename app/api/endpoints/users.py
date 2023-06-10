from fastapi import APIRouter, status, HTTPException, Header, UploadFile, File, Form
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
    CheckUsername,
    RequestAddPoints
)
from firebase_admin import auth, storage
from app.deps.firebase import db
from datetime import date, datetime
from app.deps.encrypt import encrypt, decrypt
import os

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
                'password': encrypt(request.password),
                'registeredAt': datetime.now(),
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
                if decrypt(data.get('password')) != request.password:
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
                        'registeredAt': datetime.now(),
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

@router.put("/user/{user_uid}/password", status_code=status.HTTP_200_OK)
async def update_password(
    user_uid: str,
    request: UpdatePassword
) -> JSONResponse:
    if not request.newPassword == request.confirmNewPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm new password does not match",
        )
        
    try:
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()

        if not doc_snapshot.exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )

        data = doc_snapshot.to_dict()

        if not decrypt(data.get('password')) == request.oldPassword:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect",
            )
        try:
            doc_ref.update({
                'password': encrypt(request.newPassword)
            })
            return {
                'message': 'Password updated'
            }
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

# @router.post("/user/{user_uid}/update-profile-image", status_code=status.HTTP_200_OK)
# async def upload_image(file: UploadFile = UploadFile(...)):

@router.put("/user/{user_uid}/add-points", status_code=status.HTTP_200_OK)
async def add_points(
    user_uid: str,
    request: RequestAddPoints
):
    try:
        print(user_uid)
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            data = doc_snapshot.to_dict()
            current_points = data.get('points', 0)  # Set default points to 0 if not found
            new_points = current_points + request.points

            try:
                doc_ref.update({
                    'points': new_points
                })
                return DefaultResponse(
                    message="Points added",
                    data={
                        'previous_points': current_points,
                        'points_added': request.points,
                        'points': new_points
                    }
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

@router.put("/user/{user_uid}/update-profile", status_code=status.HTTP_200_OK)
async def update_profile(user_uid: str, file: UploadFile = File(...)):
    try:
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()
        if not doc_snapshot.exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )

        data = doc_snapshot.to_dict()
        username = data.get('username')

        filename, file_extension = os.path.splitext(file.filename)

        unique_filename = f"{username}-{filename}"
        renamed_filename = f"{unique_filename}{file_extension}"

        bucket = storage.bucket()

        blob = bucket.blob(renamed_filename)
        blob.upload_from_file(file.file)
        blob.make_public()

        image_url = blob.public_url

        doc_ref.update({
            'profile_image': image_url
        })

        return {"image_url": image_url}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )