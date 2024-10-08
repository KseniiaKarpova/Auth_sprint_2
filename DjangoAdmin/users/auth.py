import http
import json

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from users.models import User as UserModel
from uuid import uuid4

User: UserModel = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        url = f"http://{settings.AUTH_API_HOST}:{settings.AUTH_API_PORT}/api/v1/auth/registration"
        payload = {'email': username, 'password': password}
        X_Request_Id = str(uuid4())
        try:
            response = requests.post(url, data=json.dumps(payload), headers={
                'X-Request-Id': X_Request_Id
            })
        except Exception as ex:
            return None
        if response.status_code != http.HTTPStatus.CONFLICT:
            return None
        data = response.json()
        try:
            user, created = User.objects.get_or_create(id=data['id'],)
            user.email = data.get('email')
            user.first_name = data.get('name')
            user.last_name = data.get('surname')
            user.is_admin = data.get('role') == 'admin'
            user.is_active = data.get('is_active')
            user.is_staff = data.get('role') == 'admin'
            user.save()
        except Exception:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
