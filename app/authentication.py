from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from app.models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        cookie_name = settings.JWT_AUTHENTICATION['COOKIE_NAME']
        if request.COOKIES.get(cookie_name):
            token = request.COOKIES.get(cookie_name)
            secret = settings.JWT_AUTHENTICATION['SECRET']
            try:
                data = jwt.decode(token, secret, algorithms=['HS256'])
                user = User.objects.get(id=data.get('id'))
            except (jwt.exceptions.InvalidTokenError, User.DoesNotExist):
                raise AuthenticationFailed
            return (user, token)
        return None