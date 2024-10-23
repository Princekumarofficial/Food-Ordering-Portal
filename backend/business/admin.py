from django.contrib import admin
from .models import Hotel, FoodItem

admin.site.register(Hotel)

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'veg', 'nonVeg')
    list_filter = ('veg', 'nonVeg')
    search_fields = ('name', 'veg', 'nonVeg')
    ordering = ('name', 'price')
    filter_horizontal = ('hotels',)
