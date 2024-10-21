# user_app/serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from common.models import MenuItem, Order, FoodItem, OrderItem    # Make sure FoodItem is imported

# Serializer for FoodItem
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'image']  # Include the fields you want to display

# User serializer for user authentication and registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields in the User model

# Serializer for MenuItem, using the FoodItemSerializer
class MenuItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()  # Use the nested FoodItem serializer

    class Meta:
        model = MenuItem
        fields = ['id', 'food_item', 'is_available']  # Adjust fields as necessary

# Serializer for Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'status', 'delivery_status', 'order_items']  # Include 'delivery_status'

# Serializer for OrderItem, used in CreateOrderSerializer
class CreateOrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())  # Expecting menu item ID

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']  # Fields for order item creation

# Serializer for creating Order with multiple OrderItems
class CreateOrderSerializer(serializers.ModelSerializer):
    order_items = CreateOrderItemSerializer(many=True)  # Accept multiple OrderItems

    class Meta:
        model = Order
        fields = ['order_items']

    def create(self, validated_data):
        # Extract order_items data
        order_items_data = validated_data.pop('order_items')
        user = self.context['request'].user  # Get the current authenticated user

        # Create the order
        order = Order.objects.create(user=user)

        # Create each order item and associate it with the order
        total_price = 0
        for item_data in order_items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            price = menu_item.food_item.price * quantity  # Calculate the price of each item

            # Create the OrderItem instance
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, price=price)
            total_price += price

        # Update total price and save the order
        order.total_price = total_price
        order.save()

        return order