from rest_framework import serializers
from django.contrib.auth.models import User
from common.models import MenuItem, Order, FoodItem,OrderItem  # Import the models for your serializers

# Admin Serializer for Signup and Login
class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should not be readable

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Adjust fields as necessary

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

# Serializer for MenuItem
class AdminMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'  # Serialize all fields

# Serializer for Order
class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # Serialize all fields

class AdminFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'description', 'image']  # Include image here

    def create(self, validated_data):
        validated_data.setdefault('is_available', True)  # Change to False if you want it to be unavailable by default

        food_item = FoodItem(**validated_data)
        food_item.save()  # Save the food item instance
        return food_item
    
class AdminOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'price']

class AdminOrderSerializer(serializers.ModelSerializer):
    order_items = AdminOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'status', 'order_items']  # Include order items