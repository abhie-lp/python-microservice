from products.views import ProductViewSet, UserAPIView
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", UserAPIView.as_view()),
] + router.urls
