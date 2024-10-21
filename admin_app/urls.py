from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminMenuItemViewSet, AdminOrderViewSet, AdminFoodItemViewSet, AdminSignupView, AdminLoginView

router = DefaultRouter()
router.register(r'menu-items', AdminMenuItemViewSet)
router.register(r'orders', AdminOrderViewSet)
router.register(r'food-items', AdminFoodItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', AdminSignupView.as_view(), name='admin-signup'),  # Admin signup
    path('login/', AdminLoginView.as_view(), name='admin-login'),      # Admin login
]
