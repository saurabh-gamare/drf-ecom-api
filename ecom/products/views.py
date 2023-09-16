from rest_framework import generics
from .serializers import ProductSerializer
from .models import Product, Category
from rest_framework.response import Response
from .paginations import ProductPagination
from rest_framework import exceptions
from ecom.utils import get_error_response


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_details = Product.objects.select_related('category').all()
        return product_details

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        paginator = ProductPagination()
        results = paginator.paginate_queryset(instance, request)
        serializer = self.get_serializer(results, many=True)
        return paginator.get_paginated_response({'product_list': serializer.data})


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')
        try:
            instance = Product.objects.get(id=product_id)
        except Exception:
            err_response = get_error_response(message='The product you are searching was not found.')
            raise exceptions.NotFound(err_response)
        serializer = self.get_serializer(instance)
        return Response({
            'product_details': serializer.data
        })


