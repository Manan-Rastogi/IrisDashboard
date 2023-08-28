import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def generate_token(username):
    print(username)
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True, payload['sub']
    except jwt.ExpiredSignatureError:
        return False, 'Signature has expired'
    except jwt.InvalidTokenError:
        return False, 'Invalid token'

