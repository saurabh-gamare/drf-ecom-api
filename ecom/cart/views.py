from rest_framework import generics
from .serializers import CouponSerializer, CartSerializer, CartItemSerializer
from .models import Coupon, Cart, CartItem
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from ecom.utils import get_error_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product


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
                print(float(product_details.mrp), 'mrp')
            except Exception:
                err_response = get_error_response(message=f'Product Id {details.get("product_id")} was not found')
                raise exceptions.NotFound(err_response)
            mrp = float(product_details.mrp) * int(details.get('quantity'))
            sale_price = float(product_details.sale_price) * int(details.get('quantity'))
            total_mrp += mrp
            total_sale_price += sale_price
        cart_details = {
            'user': request.user.id,
            'total_mrp': total_mrp,
            'total_sale_price': total_sale_price
        }
        cart_serializer = CartSerializer(data=cart_details)
        if not cart_serializer.is_valid():
            raise exceptions.ValidationError({'validation_errors': cart_serializer.errors})
        cart_instance = cart_serializer.save()
        cart_item_serializer.save(cart_instance=cart_instance)
        return Response({'cart_details': {
            'total_mrp': cart_instance.total_mrp,
            'total_sale_price': cart_instance.total_sale_price,
            'delivery_fee': cart_instance.delivery_fee,
            'total_payable': cart_instance.total_payable
        }})
