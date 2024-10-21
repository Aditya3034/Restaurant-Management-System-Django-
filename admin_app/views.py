from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from common.models import MenuItem, Order, FoodItem  # Import FoodItem
from common.serializers import MenuItemSerializer, OrderSerializer, FoodItemSerializer
from .serializers import AdminSerializer, AdminOrderSerializer  # Import AdminSerializer
from rest_framework.authtoken.models import Token

import logging
logger = logging.getLogger(__name__)

# ViewSet for managing Menu Items
class AdminMenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        food_item_id = request.data.get("food_item")
        if not food_item_id:
            return Response({"detail": "food_item is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if MenuItem with the same food_item already exists
        if MenuItem.objects.filter(food_item_id=food_item_id).exists():
            return Response({"detail": "A menu item with this food item already exists."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            food_item = FoodItem.objects.get(id=food_item_id)
        except FoodItem.DoesNotExist:
            return Response({"detail": "Food item not found."}, status=status.HTTP_404_NOT_FOUND)

        menu_item = MenuItem.objects.create(food_item=food_item)
        return Response({"id": menu_item.id, "food_item": food_item_id}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        menu_item = self.get_object()
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSet for managing Orders
class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAdminUser]  # Should restrict access to admin users only

# ViewSet for managing Food Items
class AdminFoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        logger.debug("Request data: %s", request.data)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        food_item = self.get_object()
        serializer = self.get_serializer(food_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        food_item = self.get_object()
        food_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Admin Signup View
class AdminSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminSerializer  # Your serializer for admin signup
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = True  # Set the user as an admin
            user.is_superuser = True  # Set the user as a superuser
            user.save()  # Don't forget to save the user again

            token, created = Token.objects.get_or_create(user=user)  # Create token for the user
            return Response({'username': user.username, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminLoginView(generics.GenericAPIView):
    serializer_class = AdminSerializer  # Use the same serializer for login
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Optionally, you can include views for logout or additional functionality as needed.
# views.py

class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdminUser]  # Restrict access to admin users only

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
