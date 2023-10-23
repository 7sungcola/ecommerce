import json, jwt, bcrypt, os, requests

from json import JSONDecodeError
from dotenv                 import load_dotenv

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts       import render, redirect

from .models                import User
from .validators            import Validator
from my_settings            import SECRET_KEY, ALGORITHM

from allauth.socialaccount.models import SocialAccount

load_dotenv()

BASE_URL = 'http://127.0.0.1:8000/'

KAKAO_CALLBACK_URI = BASE_URL + 'users/login/kakao/callback/'

def kakao_login(request):
    client_id = os.environ.get('KAKAO_REST_API_KEY')
    print(client_id)
    return redirect(f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code')

def kakao_callback(request):
    client_id = os.environ.get('KAKAO_REST_API_KEY')
    code = request.GET.get('code')

    token_request       = requests.get(f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}')
    token_response_json = token_request.json()

    access_token = token_response_json.get('access_token')

    profile_request = requests.post(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    profile_json = profile_request.json()

    kakao_account = profile_json.get('kakao_account')
    email = kakao_account.get('email', None)
    if email is None:
        return JsonResponse({'ERROR': 'failed to get email'}, status=400)

def index(request):
    return render(request, 'user/index.html', {})

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)

            email           = data['email']
            password        = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'ERROR' : 'Account already exists'}, status=400)

            validator = Validator()
            validator.validate_email(email)
            validator.validate_password(password)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = email,
                password = hashed_password
            )

            return JsonResponse({'MESSAGE' : 'Created'}, status=201)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)

            email           = data['email']
            password        = data['password']

            validator = Validator()
            validator.validate_email(email)
            validator.validate_password(password)

            user            = User.objects.get(email=email)
            hashed_password = user.password.encode('utf-8')

            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return JsonResponse({'ERROR' : 'Failed to Login'}, status=400)

            payload = {'id' : user.id}
            token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)

            return JsonResponse({'MESSAGE' : 'Success', 'TOKEN' : token}, status=200)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'ERROR' : 'Failed to Login'}, status=400)