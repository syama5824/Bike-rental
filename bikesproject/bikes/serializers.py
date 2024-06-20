from rest_framework import serializers
from .models import Bike,Users

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'contact', 'email', 'created_at', 'updated_at', 'is_admin', 'user_role', 'age', 'aadhar_number', 'driving_license']
