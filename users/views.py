from base64 import encode
import json, jwt, bcrypt

from datetime import datetime, timedelta

from django.forms import ValidationError
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from users.vallidator import validate_data,hashed_password,checked_password,access_token
from users.models import User



class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']
            email    = data['email']

            validate_data(username,email,password)
            
            if User.objects.filter(username = username).exists(): 
                return JsonResponse({'message' : 'Username already exists'}, status=409)

            if User.objects.filter(email = email).exists(): 
                return JsonResponse({'message' : 'Email already exists'}, status=409)

            user, is_created = User.objects.get_or_create(
                username = username,
                email = email,
                password = hashed_password(password)
            )

            return JsonResponse({"message" : "Success"}, status=201)

        except KeyError: 
            return JsonResponse({'message' : 'Key error'}, status=400)

        except ValidationError as e: 
            return JsonResponse({'message' : e.message}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            user = User.objects.get(username=username)

            checked_password(password,user)
        
            return JsonResponse({'token' : access_token(user)}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'User does not exist'}, status=401)
        
        except KeyError:
            return JsonResponse({'message' : 'Key error'}, status=400)