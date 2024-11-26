from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password', 
            'name', 
            'birth_date',
            'phone', 
            'address', 
            'detail_address',
            'annual_salary', 
            'asset'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'annual_salary': {'required': False},
            'asset': {'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'name', 
            'birth_date',
            'phone', 
            'address', 
            'detail_address',
            'annual_salary', 
            'asset'
        )