from random import choice
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Product, User
from .producer import publish
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        publish("product_created", response.data)
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        publish("product_updated", response.data)
        return response
    
    def destroy(self, request, *args, **kwargs):
        publish("product_deleted", self.get_object().pk)
        return super().destroy(request, *args, **kwargs)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = choice(users)
        return Response({"id": user.id})