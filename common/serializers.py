from rest_framework import serializers
from .models import MenuItem, Order, FoodItem, OrderItem  # Import FoodItem model

# Serializer for FoodItem
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available']  # Define the fields

# Serializer for MenuItem
class MenuItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()  # Nest FoodItemSerializer

    class Meta:
        model = MenuItem
        fields = ['id', 'food_item', 'is_available']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'price']

# Serializer for Order
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # Remove read_only=True to allow creation

    class Meta:
        model = Order
        fields = ['user', 'created_at', 'total_price', 'status', 'delivery_status', 'order_items']  # Include 'delivery_status'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        user = self.context['request'].user  # Ensure we are creating the order for the authenticated user
        order = Order.objects.create(user=user, **validated_data)  # Create the order
        total_price = 0

        # Loop through each order item, create it, and calculate the total price
        for item_data in order_items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            price = menu_item.food_item.price * quantity  # Calculate price based on the food item's price

            # Create OrderItem and associate it with the order
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, price=price)
            total_price += price

        # Set the total price and save the order
        order.total_price = total_price
        order.save()

        return order
