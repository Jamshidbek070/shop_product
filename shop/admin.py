from django.contrib import admin
from .models import Category, Product, ProductImage, UserProfile, Comment, Like, Rating

# 1️⃣ Kategoriya admini
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ['name']
    list_filter = ('created_at', 'updated_at')

# 2️⃣ Mahsulot admini
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ['name', 'description']
    list_filter = ('category', 'created_at', 'updated_at')

# 3️⃣ Mahsulot rasmlari admini
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at')
    search_fields = ['product__name']
    list_filter = ('created_at',)

# 4️⃣ Foydalanuvchi profili admini
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_at', 'updated_at')
    search_fields = ['user__username']
    list_filter = ('created_at', 'updated_at')

# 5️⃣ Izohlar admini
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'created_at')
    search_fields = ['text']
    list_filter = ('created_at',)

# 6️⃣ Layklar admini
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)

# 7️⃣ Reytinglar admini
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'stars', 'created_at')
    list_filter = ('created_at', 'stars')
    search_fields = ['user__username', 'product__name']
