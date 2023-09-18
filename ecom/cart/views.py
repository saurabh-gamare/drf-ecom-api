from rest_framework import generics
from .serializers import CouponSerializer, CartSerializer, CartItemSerializer, AddressSerializer
from .models import Coupon, Cart, CartItem, Address
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from ecom.utils import get_error_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from rest_framework import mixins


class CouponList(generics.ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response({
            'coupons': serializer.data
        })


class CartDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_item_serializer = CartItemSerializer(data=request.data)
        if not cart_item_serializer.is_valid():
            raise exceptions.ValidationError({'validation_errors': cart_item_serializer.errors})
        cart_details = request.data.get('cart_details')
        total_mrp, total_sale_price = 0.0, 0.0
        for details in cart_details:
            try:
                product_details = Product.objects.get(id=details.get('product_id'))
            except Exception:
                err_response = get_error_response(message=f'Product Id {details.get("product_id")} was not found')
                raise exceptions.NotFound(err_response)
            mrp = float(product_details.mrp) * int(details.get('quantity'))
            sale_price = float(product_details.sale_price) * int(details.get('quantity'))
            total_mrp += mrp
            total_sale_price += sale_price
        cart_details = {
            'user': request.user.id,
            'total_mrp': round(total_mrp, 2),
            'total_sale_price': round(total_sale_price, 2)
        }
        cart_serializer = CartSerializer(data=cart_details)
        if not cart_serializer.is_valid():
            raise exceptions.ValidationError({'validation_errors': cart_serializer.errors})
        cart_instance = cart_serializer.save()
        cart_item_serializer.save(cart_instance=cart_instance)
        return Response({'cart_details': {
            'total_mrp': round(cart_instance.total_mrp, 2),
            'total_sale_price': round(cart_instance.total_sale_price, 2),
            'delivery_fee': cart_instance.delivery_fee,
            'total_payable': round(cart_instance.total_payable, 2)
        }})


class AddressCreateListMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationError({'validation_errors': serializer.errors})
        self.perform_create(serializer)
        return Response({'message': 'Address created'})

    def list(self, request, *args, **kwargs):
        queryset = Address.objects.filter(user=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'address_list': serializer.data
        })

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AddressRetrieveUpdateDestroyMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_address_object(self, request, *args, **kwargs):
        try:
            address_object = Address.objects.get(user=request.user.id, id=kwargs.get('pk'))
        except Exception:
            err_response = get_error_response(message='Address not found')
            raise exceptions.NotFound(err_response)
        return address_object

    def retrieve(self, request, *args, **kwargs):
        address_object = self.get_address_object(request, *args, **kwargs)
        serializer = self.get_serializer(address_object)
        return Response({'address_details': serializer.data})

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        address_object = self.get_address_object(request, *args, **kwargs)
        serializer = self.get_serializer(address_object, data=request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationError({'message': serializer.errors})
        self.perform_update(serializer)
        return Response({'message': f'Address updated'})

    def destroy(self, request, *args, **kwargs):
        address_object = self.get_address_object(request, *args, **kwargs)
        self.perform_destroy(address_object)
        return Response({'message': 'Address deleted'})

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
