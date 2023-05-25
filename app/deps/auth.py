from fastapi import FastAPI, HTTPException, Depends
from firebase_admin import auth, credentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

# Load Firebase Admin SDK credentials
cred = credentials.Certificate("ServiceAccountKey.json")
auth.initialize_app(cred)

# Create a FastAPI security dependency for ID token authentication
security = HTTPBearer()

# Middleware to verify and extract the authenticated user from the ID token
async def authenticate_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Verify and decode the ID token
        decoded_token = auth.verify_id_token(token.credentials)
        # Extract user ID or other desired user information from the decoded token
        user_id = decoded_token['uid']
        # You can perform additional checks or fetch user details from a database

        # Return the authenticated user or raise an exception if not authenticated
        return user_id

    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Expired ID token")
    except auth.RevokedIdTokenError:
        raise HTTPException(status_code=401, detail="Revoked ID token")