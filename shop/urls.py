from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView, ProductDetailView, ProductImageUploadView,
    CategoryListView, CategoryDetailView,
    CommentCreateView, LikeCreateView, RatingCreateView,
    UserProfileView, WishlistView, AdminProductCreateView,
    RegisterView, LoginView, LogoutView, CartView, OrderAPIView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Swagger schema yaratish
schema_view = get_schema_view(
   openapi.Info(
      title="OILAM UCHUN E-Commerce API",
      default_version='v1',
      description="API hujjati",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@oilamuchun.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

# URL'lar ro'yxati
urlpatterns = [
    # Kategoriya URL'lari
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Mahsulot URL'lari
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-images/', ProductImageUploadView.as_view(), name='product-image-upload'),

    
    # Izoh URL'lari
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    
    # Layk URL'lari
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    
    # Reyting URL'lari
    path('ratings/', RatingCreateView.as_view(), name='rating-create'),
    
    # Foydalanuvchi profili URL'lari
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Wishlist URL'lari
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    
    # Admin mahsulot qo'shish URL'i
    path('admin/products/', AdminProductCreateView.as_view(), name='admin-product-create'),
    
    # Ro‘yxatdan o‘tish va Login URL'lari
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Swagger API hujjatlari uchun URL
    path('swagger/', schema_view.as_view(), name='swagger'),  # Swagger URL qo'shish
    # Savatcha
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderAPIView.as_view(), name='orders'),
]
