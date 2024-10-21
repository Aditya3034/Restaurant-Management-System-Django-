# user_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserLoginView, UserSignupView, TestTokenView, OrderViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')  # Register the OrderViewSet
router.register(r'menu-items', MenuItemViewSet, basename='menu-item')  # Register the MenuItemViewSet

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('test_token/', TestTokenView.as_view(), name='test-token'),
    path('', include(router.urls)),  # Include all router URLs
]
