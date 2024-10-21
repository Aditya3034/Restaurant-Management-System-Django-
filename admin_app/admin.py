from django.contrib import admin
from common.models import FoodItem,Order  

# Register FoodItem to appear in the Django admin panel
@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available']  # Customize the list display in admin
    search_fields = ['name']
    list_filter = ['is_available']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price', 'status', 'delivery_status')
    list_filter = ('status', 'delivery_status')

admin.site.register(Order, OrderAdmin)