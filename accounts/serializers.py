from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'username']
        model = User
    
    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.pop('password2', None)

        if password != password_confirmation:
            raise serializers.ValidationError({'password2': 'Passwords do not match'})

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e})
        return super().validate(data)