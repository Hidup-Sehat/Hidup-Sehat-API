import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os
import json

load_dotenv()

# cred = credentials.Certificate({
#     "type": os.getenv("FIREBASE_TYPE"),
#     "project_id": os.getenv("FIREBASE_PROJECT_ID"),
#     "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
#     "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
#     "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
#     "client_id": os.getenv("FIREBASE_CLIENT_ID"),
#     "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
#     "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
#     "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
#     "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
#     "universal_domain": os.getenv("FIREBASE_UNIVERSAL_DOMAIN")
# })
# env = os.getenv("FIREBASE")
# envdump = json.dumps(env)
# print(env, envdump)

# print(os.getenv("FIREBASE"))
data = json.loads(os.getenv("FIREBASE"))
cred = credentials.Certificate(data)
#meme
firebase_admin.initialize_app(cred, {'storageBucket': 'hidup-sehat-server.appspot.com'})
db = firestore.client()