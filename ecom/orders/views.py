from rest_framework import generics
from rest_framework.response import Response
from .models import Order, OrderItem
from cart.models import Cart, CartItem, Address
from .serializers import OrderSerializer, OrderItemSerializer, ListOrderSerializer, RetrieveOrderSerializer
from cart.serializers import CartSerializer, CartItemSerializer, AddressSerializer
from rest_framework.views import APIView
from rest_framework import exceptions
from ecom.utils import get_error_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from rest_framework import mixins
from django.forms.models import model_to_dict
from .paginations import OrderPagination
import random, string


class CreateOrder(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            Address.objects.get(user=request.user, id=request.data.get('address_id'))
        except Exception:
            err_response = get_error_response(message='Address not found')
            raise exceptions.NotFound(err_response)
        order_serializer = OrderSerializer(data=request.data)
        if not order_serializer.is_valid():
            raise exceptions.ValidationError({'validation_errors': order_serializer.errors})
        cart_item_instance = CartItem.objects.select_related('user').filter(user__user=request.user)
        try:
            cart_instance = Cart.objects.get(user=request.user)
        except Exception:
            err_response = get_error_response(message='Cart is empty')
            raise exceptions.NotFound(err_response)
        for details in cart_item_instance.values():
            product_id = details.get('product_id')
            quantity = int(details.get('quantity'))
            product_instance = Product.objects.filter(id=product_id)
            current_stock = int(product_instance[0].stock_qty)
            if current_stock < quantity:
                err_response = get_error_response(message='One of the product(s) is out of stock')
                raise exceptions.NotAcceptable(err_response)
            updated_stock = current_stock - quantity
            product_instance.update(stock_qty=updated_stock)
        cart_serializer = CartSerializer(cart_instance)
        order_data = cart_serializer.data
        order_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        order_data.update({
            'order_id': order_id,
            'user': request.user
        })
        order_data.pop('id')
        order_instance = order_serializer.save(**order_data)
        for details in cart_item_instance.values():
            order_item_serializer = OrderItemSerializer(data=details)
            if not order_item_serializer.is_valid():
                raise exceptions.ValidationError({'validation_errors': order_item_serializer.errors})
            order_item_data = {
                'order_id': order_instance,
                'user': request.user
            }
            order_item_serializer.save(**order_item_data)
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': 'Order placed'})


class ListOrders(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = ListOrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Order.objects.filter(user=kwargs.get('user'))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(user=request.user)
        paginator = OrderPagination()
        instance = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(instance, many=True)
        return paginator.get_paginated_response({
            'orders': serializer.data
        })


class RetrieveOrder(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = RetrieveOrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, *args, **kwargs):
        try:
            instance = Order.objects.get(user=kwargs.get('user'), order_id=kwargs.get('order_id'))
        except Exception:
            err_response = get_error_response(message='Order not found')
            raise exceptions.NotFound(err_response)
        return instance

    def retrieve(self, request, *args, **kwargs):
        order_id = request.query_params.get('order')
        if not order_id:
            err_response = get_error_response(message='Order not found')
            raise exceptions.NotFound(err_response)
        instance = self.get_object(user=request.user, order_id=order_id)
        serializer = self.get_serializer(instance)
        return Response({'order': serializer.data})
