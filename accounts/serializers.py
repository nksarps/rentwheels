from .models import User
from datetime import date
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'username', 'email', 'phone_number', 'password']

        read_only_fields = ['id']


    def validate(self, attrs):
        dob = attrs.get('date_of_birth')
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 18:
            raise serializers.ValidationError('You must be atleast 18 to register', code='age')

        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials', code='authentication')

        attrs['user'] = user
        return attrs

    def generate_token(self, attrs):
        user = attrs.get('user')

        refresh = RefreshToken.for_user(user)

        tokens = {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

        return tokens


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'username', 'email', 'phone_number']

        read_only_fields = ['id']