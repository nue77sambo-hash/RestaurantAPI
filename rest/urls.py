from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, CustomLoginView, CategoryViewSet, MenuItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menu', MenuItemViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('login/', CustomLoginView.as_view(), name = 'login'),
    path('', include(router.urls)),
]