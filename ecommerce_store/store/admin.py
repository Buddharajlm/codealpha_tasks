from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'stock', 'is_available', 'rating', 'created_at')
    list_filter = ('category', 'is_available', 'created_at')
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'get_cost')

    def get_cost(self, obj):
        return f"${obj.get_cost():.2f}"
    get_cost.short_description = 'Item Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone')
    readonly_fields = ('order_number', 'subtotal', 'shipping_cost', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
