import re, bcrypt, jwt
from django.forms import ValidationError
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timedelta

REGEX_USERNAME = '^[a-z0-9+]{3,15}$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$'
REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def validate_data(username,email,password):
    if not re.match(REGEX_USERNAME, username):
        raise ValidationError("Invalid username")

    if not re.match(REGEX_EMAIL, email):
        raise ValidationError("Invalid email")

    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError("Invalid password")


def hashed_password(password):
    hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    return hash_password


def checked_password(password,user):
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return JsonResponse({'message' : 'Password does not match'}, status=401)

def access_token(user):
    access_token = jwt.encode({"id":user.id, 'exp':datetime.utcnow()+timedelta(days=3)}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return access_token