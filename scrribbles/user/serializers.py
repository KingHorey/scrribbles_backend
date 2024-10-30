from rest_framework import serializers
from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserLoginSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)

		token['id'] = str(user.id)
		# user['email'] = user.email
		token['first_name'] = user.first_name
		token['last_name'] = user.last_name

		return token

class RegisterUserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'password']

	def create(self, data):
		""" overide the method of creating a user"""
		user = User.objects.create_user(email=data.get("email"), password=data.get("password"), first_name=data.get("first_name"), last_name=data.get("last_name"))
		return user

class UserInformationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ["id", "first_name", "last_name", "email", "password", "profile_image"]

	def update(self, instance, validated_data):
		new_password = validated_data.pop("new_password", [])
		confirmed_password = validated_data.pop("confirm_password", [])
		user_id = validated_data.pop("id", [])
		if new_password:
			instance.set_password(new_password)
		user = super().update(instance, validated_data)
		print(user)

		return user
