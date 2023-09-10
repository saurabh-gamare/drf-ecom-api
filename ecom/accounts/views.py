from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AuthSerializer
from django.core.mail import send_mail
from rest_framework import exceptions, permissions
from django.conf import settings
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from ecom.utils import get_error_response


User = get_user_model()


class Auth(APIView):

    def send_otp_via_email(self, otp, receiver_email):
        subject = f'ECOM One-Time Password for Login: [{otp}]'
        message = ''
        html_message = f'''
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>OTP for your Django Project</title>
            </head>
            <body>
                <h2 style='text-align:center'>OTP for your ECOM Project</h2>
                <p style='text-align:center'>Please use this OTP to verify your account.</p>
                <h1 style='text-align:center'>{otp}</h1>
            </body>
            </html>
        '''
        sender_email = settings.EMAIL_HOST_USER
        receiver_emails = [receiver_email]
        send_mail(subject, message, sender_email, receiver_emails, html_message=html_message)

    def post(self, request):
        data = request.data
        if not data.get('email'):
            err_response = get_error_response(message='Email is required')
            raise exceptions.ValidationError(err_response)
        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationError({'validation_errors': serializer.errors})
        otp = str(random.randint(1000, 9999))
        receiver_email = serializer.validated_data.get('email')
        try:
            self.send_otp_via_email(otp, receiver_email)
        except Exception as e:
            err_response = get_error_response(error_code=1001, error=str(e))
            raise exceptions.ValidationError(err_response)
        serializer.save(otp=otp)
        return Response({
            'message': 'OTP sent'
        })


class Login(APIView):

    def check_required_fields(self, email, otp):
        if not email:
            err_response = get_error_response(message='Email is required')
            raise exceptions.ValidationError(err_response)
        if not otp:
            err_response = get_error_response(message='OTP is required')
            raise exceptions.ValidationError(err_response)

    def get(self, request):
        data = request.data
        email = data.get('email')
        otp = data.get('otp')
        self.check_required_fields(email, otp)
        user_instance = User.objects.get(email=email)
        if str(otp) != str(user_instance.otp):
            err_response = get_error_response(message='Please enter correct OTP')
            raise exceptions.ValidationError(err_response)
        User.objects.filter(email=email).update(otp=None)
        refresh = RefreshToken.for_user(user_instance)
        return Response({
            'message': 'Success',
            'response': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        })


class Test(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'response': request.data})

