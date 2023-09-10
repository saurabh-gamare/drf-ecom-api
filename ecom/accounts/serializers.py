from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'mobile',
            'otp'
        ]

    def create(self, validated_data):
        email = validated_data.get('email')
        otp = validated_data.get('otp')
        user = User.objects.filter(email=email)
        if not user.exists():
            user = User(username=email, email=email)
            user.save()
        User.objects.filter(email=email).update(otp=otp)
        return user

    def validate(self, data):
        # raise serializers.ValidationError({'email': "Email address is already in use."})
        return data
