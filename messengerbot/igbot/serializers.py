from rest_framework import serializers
from .models import Instagrammer

class InstagrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instagrammer
        fields = '__all__'