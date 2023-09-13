from rest_framework import generics
from .serializers import ProductSerializer
from .models import Product, Category
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_details = Product.objects.select_related('category').all()
        return product_details

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(instance, request)
        serializer = self.get_serializer(results, many=True)
        return paginator.get_paginated_response({'product_list': serializer.data})
