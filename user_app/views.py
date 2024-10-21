from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, MenuItemSerializer, OrderSerializer,CreateOrderSerializer  # Import OrderSerializer
from common.models  import MenuItem, Order, OrderItem
# SignUp View
class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])  # Set hashed password
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = self.get_serializer(user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)

# ViewSet for Menu Items
class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.filter(is_available=True)  # Only show available menu items
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer  # Use CreateOrderSerializer for creating orders
        return OrderSerializer  # Use OrderSerializer for other actions

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # Return only user's orders


# Test Token View
class TestTokenView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response("Token is valid!", status=status.HTTP_200_OK)
