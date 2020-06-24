from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import AuthenticationSerializer
import jwt
from django.conf import settings


class AuthenticationView(APIView):

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            userData = serializer.validated_data
            payload = {'id': userData['id']}
            secret = settings.JWT_AUTHENTICATION['SECRET']
            token = jwt.encode(payload, secret, algorithm='HS256')
            token = token.decode('utf-8')
            response = Response(userData)
            cookie_name = settings.JWT_AUTHENTICATION['COOKIE_NAME']
            response.set_cookie(cookie_name, value=token, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def get(self, request):
        data = {'message': 'Successfully logged out.'}
        response = Response(data)
        cookie_name = settings.JWT_AUTHENTICATION['COOKIE_NAME']
        response.delete_cookie(cookie_name)
        return response