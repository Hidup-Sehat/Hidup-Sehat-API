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
    GetWeeklyLeaderboard,
    GetMonthlyLeaderboard,
    GetUserData,
    CheckUsername,
    RequestAddPoints
)
from firebase_admin import auth, storage
from app.deps.firebase import db
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.deps.encrypt import encrypt, decrypt
from app.deps.leaderboard import (
    get_week_id, 
    get_month_id, 
    update_total_points, 
    update_weekly_points, 
    update_monthly_points,
    update_weekly_leaderboard, 
    update_monthly_leaderboard
)
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
        defaultProfilePic="https://firebasestorage.googleapis.com/v0/b/hidup-sehat-server.appspot.com/o/blank-profile.png?alt=media&token=416c3ef1-8c69-453c-b9c6-e35e390102b8&_gl=1*1z115oz*_ga*MjAzMzY5MDczOC4xNjg1MDM0NTY1*_ga_CW55HF8NVT*MTY4NjQxMTQyOC4yNC4xLjE2ODY0MTIyNjUuMC4wLjA."
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
                'imgUrl': defaultProfilePic,
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

@router.get("/weekly-leaderboard", response_model=GetWeeklyLeaderboard , status_code=status.HTTP_200_OK)
async def get_leaderboard() -> GetWeeklyLeaderboard:
    try:
        today = datetime.now().date()
        current_week_start = today - timedelta(days=today.weekday())
        current_week_end = current_week_start + timedelta(days=6)
        week_id = f"{current_week_start.strftime('%d-%m-%Y')}_{current_week_end.strftime('%d-%m-%Y')}"
        print(week_id)

        doc_ref = db.collection('weekly-leaderboard').document(week_id)
        leaderboard_doc = doc_ref.get()

        if leaderboard_doc.exists:
            leaderboard = leaderboard_doc.get('leaderboard')
            return GetWeeklyLeaderboard(
                _id = week_id,
                weekStartDate = leaderboard_doc.get('weekStartDate'),
                weekEndDate = leaderboard_doc.get('weekEndDate'),
                data = leaderboard
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get("/monthly-leaderboard", response_model=GetMonthlyLeaderboard, status_code=status.HTTP_200_OK)
async def get_monthly_leaderboard() -> GetMonthlyLeaderboard:
    try:
        today = datetime.now().date()
        current_month_start = today.replace(day=1)
        current_month_end = (current_month_start + relativedelta(months=1) - timedelta(days=1))
        month_id = current_month_start.strftime('%m-%Y')

        doc_ref = db.collection('monthly-leaderboard').document(month_id)
        leaderboard_doc = doc_ref.get()

        if leaderboard_doc.exists:
            leaderboard = leaderboard_doc.get('leaderboard')
            return GetMonthlyLeaderboard(
                _id=month_id,
                monthStartDate=leaderboard_doc.get('monthStartDate'),
                monthEndDate=leaderboard_doc.get('monthEndDate'),
                data=leaderboard
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Monthly leaderboard not found"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
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

@router.get("/user/{user_uid}/point", status_code=status.HTTP_200_OK)
async def get_points(
    user_uid: str
):
    try:
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            data = doc_snapshot.to_dict()
            return {
                'total-points': data.get('totalPoints', 0)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
)

@router.put("/user/{user_uid}/point", status_code=status.HTTP_200_OK)
async def add_points(
    user_uid: str,
    request: RequestAddPoints
):
    try:
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        weekly_point_id = f"{start_of_week.strftime('%d-%m-%Y')}_{end_of_week.strftime('%d-%m-%Y')}"

        # Calculate the monthly point ID
        month_year = today.strftime('%m-%Y')
        monthly_point_id = month_year

        user_ref = db.collection('users').document(user_uid)
        doc_snapshot = user_ref.get()

        if doc_snapshot.exists:
            weekly_point_id = get_week_id()
            monthly_point_id = get_month_id()
            data = doc_snapshot.to_dict()

            # Update total points
            new_total_point = update_total_points(user_uid, request.points)

            # Update weekly points
            combined_weekly_points = update_weekly_points(user_uid, weekly_point_id, request.points)

            # Update monthly points
            combined_monthly_points = update_monthly_points(user_uid, monthly_point_id, request.points)

            update_weekly_leaderboard(user_uid, data.get('username'), data.get('imgUrl'), request.points)

            update_monthly_leaderboard(user_uid, data.get('username'), data.get('imgUrl'), request.points)

            return DefaultResponse(
                message="Points added",
                data={
                    'previous_points': data.get('totalPoints', 0),
                    'points_added': request.points,
                    'points': new_total_point
                }
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
            'imgUrl': image_url
        })

        return {"image_url": image_url}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )