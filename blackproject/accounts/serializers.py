# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser , STOCK

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            # image=validated_data['image']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = STOCK
        fields =[ 'stockcode','stockname','quant','ltp']
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = STOCK(
            # user=validated_data['username'],
            stockcode=validated_data['stockcode'],
            stockname=validated_data['stockname'],
            ltp=validated_data['ltp'],
            quant=validated_data['quant'],
            # image=validated_data['image']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user