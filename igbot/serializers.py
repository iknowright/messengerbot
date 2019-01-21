from rest_framework import serializers
from .models import Instagrammer
from .models import Token

class InstagrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instagrammer
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'