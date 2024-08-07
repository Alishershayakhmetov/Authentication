from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OtpToken, CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

from .serializers import CustomUserRegistrationSerializer, OTPVerificationSerializer


# Create your views here.

class CustomUserRegistration(APIView):
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerify(APIView):
    def post(self, request, email):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            try:
                otp = OtpToken.objects.get(otp_code=otp_code, otp_expires_at__gte=timezone.now(), user__email=email)
                user = otp.user
                user.email_verified = True
                user.is_active = True
                user.save()
                otp.delete()
                return Response({'message': 'Account verified and activated.'}, status=status.HTTP_200_OK)
            except OtpToken.DoesNotExist:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

