from rest_framework import viewsets, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Category, MenuItem, Order, OrderItem
from .serializers import (UserRegistrationSerializer, CategorySerializer, MenueItemSerializer, OrderSerializer)
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token' : token.key,
            'user_id' : user.pk,
            'username' : user.username,
            'is_staff' : user.is_staff
        }, status=status.HTTP_201_CREATED)

class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username = username, password = password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token' : token.key,
                'user_id' : user.pk,
                'username' : user.username,
                'is_staff' : user.is_staff
                }, status=status.HTTP_200_OK)
        return Response({'error': "invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


# class CustomLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         self.response = super().post(request, *args, **kwargs)
#         token = Token.objects.get(key=self.response.data['token'])
#         user = token.user
#         return Response({
#             'token' : token.key,
#             'user_id' : user.pk,
#             'username' : user.username,
#             'is_staff' : user.is_staff
#         })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return[permissions.AllowAny()]
        return super().get_permissions()


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenueItemSerializer
    filterset_fields = ['category', 'is_available']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')
