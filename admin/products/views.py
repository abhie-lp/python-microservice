from random import choice
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Product, User
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = choice(users)
        return Response({"id": user.id})