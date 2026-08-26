import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

def get_firestore_client():
    if not firebase_admin._apps:
        # Karanta gaba ɗayan JSON ɗin daga .env
        service_account_env = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        
        if not service_account_env:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON ba ya cikin .env fayil!")
            
        # Mayar da shi zuwa dictionary
        service_account_info = json.loads(service_account_env)
        
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)

    return firestore.client()