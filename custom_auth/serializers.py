from rest_framework import serializers
from .models import OtpToken, CustomUser

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        return user

class OTPVerificationSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)
