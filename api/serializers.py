from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.spots import Spot
from .models.user import User

class SpotSerializer(serializers.ModelSerializer):
  class Meta:
    model = Spot
    fields = ('id', 'country', 'state', 'state', 'city', 'description', 'season', 'owner')

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('id', 'email', 'password')
    extra_kwargs = { 'password': { 'wrtie_only': True, 'min_length': 5 } }

  def create(self, validated_data):
    return get_user_model().objects.create_user(**validated_data)

class UserLoginSerializer(UserSerializer):
  email = serializers.CharField(max_length=300, required=True)
  password = serializers.CharField(required=True, write_only=True)

class UserRegisterSerializer(serializers.Serializer):
  email = serializers.CharField(max_length=300, required=True)
  password = serializers.CharField(required=True)
  password_confirmation = serializers.CharField(required=True, write_only=True)

  def validate(self, data):
    if not data['password'] or not data['password_confirmation']:
      raise serializers.ValidationError('Please include a password and password confirmation.')

    if data['password'] != data['password_confirmation']:
      raise serializers.ValidationError('Please make sure your passwords match.')

    return data

class ChangePasswordSerializer(serializers.Serializer):
  model = get_user_model()
  old = serializers.CharField(required=True)
  new = serializers.CharField(required=True)
