from django.contrib import admin
from .models import EcoProduct, EcoTip, UserUpload, UserHistory, SustainabilityCalculator
from .models import Order

@admin.register(EcoProduct)
class EcoProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_eco_friendly', 'created_at')
    list_filter = ('category', 'is_eco_friendly', 'created_at')
    search_fields = ('name', 'description')

@admin.register(EcoTip)
class EcoTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')

@admin.register(UserUpload)
class UserUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('title', 'description')

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'page_visited', 'visit_date')
    list_filter = ('visit_date',)
    search_fields = ('user__username', 'page_visited')

@admin.register(SustainabilityCalculator)
class SustainabilityCalculatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'carbon_footprint', 'calculated_at')
    list_filter = ('calculated_at',)
    search_fields = ('user__username',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'product', 'quantity', 'order_date', 'status')
    search_fields = ('order_id', 'user__username', 'product__name')