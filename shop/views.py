from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  (Category, Product, ProductImage, UserProfile, 
    Comment, Like, Rating, CartItem, Order, OrderItem)
from .serializers import (
    CategorySerializer, ProductSerializer, ProductImageSerializer,
    UserProfileSerializer, CommentSerializer, LikeSerializer, RatingSerializer,
    RegisterSerializer, LoginSerializer, CartItemSerializer,
    OrderSerializer
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

# 1️⃣ Kategoriya API (List va Detail)
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# 2️⃣ Mahsulot API (List, Detail)
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter



class ProductImageUploadView(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# 3️⃣ Izoh API (Create va List)
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        serializer.save(user=self.request.user, product=product)


# 4️⃣ Layk API (Create va List)
class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        serializer.save(user=self.request.user, product=product)


# 5️⃣ Reyting API (Create va List)
class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        serializer.save(user=self.request.user, product=product)


# 6️⃣ Foydalanuvchi profili (GET va Update)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# 7️⃣ Wishlist API (Add va Remove mahsulotlar)
class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProductSerializer(profile.wishlist.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        product = Product.objects.get(id=request.data['product_id'])
        request.user.profile.wishlist.add(product)
        return Response({'status': 'added to wishlist'}, status=201)

    def delete(self, request):
        product = Product.objects.get(id=request.data['product_id'])
        request.user.profile.wishlist.remove(product)
        return Response({'status': 'removed from wishlist'}, status=204)


# 8️⃣ Admin mahsulot qo‘shish uchun faqat admin
class AdminProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({
                'user': RegisterSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 9️⃣ Foydalanuvchi tizimga kirish (Login)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=serializer.validated_data['username']).first()
            if user and user.check_password(serializer.validated_data['password']):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'user': RegisterSerializer(user).data,
                    'token': token.key
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Foydalanuvchining tokenini o‘chiradi
            request.user.auth_token.delete()
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
        
        
# 🔟 Foydalanuvchi uchun shopping savatchasi
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        product = Product.objects.get(id=product_id)
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            item.quantity += int(quantity)
        else:
            item.quantity = int(quantity)
        item.save()
        return Response({'status': 'added', 'item_id': item.id}, status=201)

    def delete(self, request):
        product_id = request.data.get('product')
        try:
            item = CartItem.objects.get(user=request.user, product__id=product_id)
            item.delete()
            return Response({'status': 'removed'}, status=204)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)
        
# 1️⃣1️⃣ Foydalanuvchi uchun shopping
class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Savatcha bo‘sh'}, status=400)

        # Yangi buyurtma yaratish
        order = Order.objects.create(user=request.user)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        # Savatchani tozalash
        cart_items.delete()

        return Response({'status': 'Buyurtma yaratildi'}, status=201)

