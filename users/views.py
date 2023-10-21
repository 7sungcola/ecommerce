import json, jwt, bcrypt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts       import render

from .models                import User
from .validators            import Validator
from my_settings            import SECRET_KEY, ALGORITHM


def index(request):
    return render(request, 'user/index.html', {})

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)

            email           = data['email']
            password        = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'Account already exists'}, status = 400)

            validator = Validator()
            validator.validate_email(email)
            validator.validate_password(password)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = email,
                password = hashed_password
            )

            return JsonResponse({'MESSAGE' : 'Created'}, status = 201)

        except ValidationError as e:
            return JsonResponse({'MESSAGE' : e.message}, status = 400)

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
                return JsonResponse({'MESSAGE' : 'Failed to Login'}, status = 400)

            payload = {'id' : user.id}
            token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)

            return JsonResponse({'MESSAGE' : 'Success', 'TOKEN' : token}, status = 200)

        except ValidationError as e:
            return JsonResponse({'MESSAGE' : e.message}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'Failed to Login'}, status = 400)