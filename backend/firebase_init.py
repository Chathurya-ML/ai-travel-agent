import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

firebase_cred = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY"), #.replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI")

}

# cred = credentials.Certificate("C:\AITravel\service_account.json")
firebase_admin.initialize_app(firebase_cred)
db = firestore.client()