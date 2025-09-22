import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Construct the Firebase credentials from environment variables
firebase_cred = {
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),#.replace("\\n", "\n"),  # Replace escaped newlines
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")  
}
print("Firebase credentials loaded:")
for key, value in firebase_cred.items():
    print(f"{key}: {value}")
print("Private key preview:", firebase_cred["private_key"][:30] + '...' if firebase_cred["private_key"] else "None")
# Initialize Firebase Admin with the constructed credentials
cred = credentials.Certificate(firebase_cred)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()