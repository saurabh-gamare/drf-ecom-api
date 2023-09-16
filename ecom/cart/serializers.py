from rest_framework import serializers
from . import models


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    delivery_fee = serializers.IntegerField(read_only=True)
    total_payable = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = models.Cart
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.get('user').id
        try:
            cart_details = models.Cart.objects.get(user=user)
        except:
            cart = models.Cart(**validated_data)
            cart.save()
            cart_details = models.Cart.objects.get(user=user)
        return cart_details

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_payable'] = float(data['total_payable'])
        data['coupon_discount'] = float(data['coupon_discount'])
        data['total_mrp'] = float(data['total_mrp'])
        data['total_sale_price'] = float(data['total_sale_price'])
        return data


class CartProductDetailSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = models.CartItem
        fields = ['product_id', 'quantity']


class CartItemSerializer(serializers.Serializer):
    cart_details = CartProductDetailSerializer(many=True)

    def create(self, validated_data):
        cart_instance = validated_data.get('cart_instance')
        print(cart_instance, 'cart_instance')
        for details in validated_data.get('cart_details'):
            try:
                models.CartItem.objects.get(user=cart_instance, product_id=details.get('product_id'))
            except:
                details.update({'user': cart_instance})
                cart_item = models.CartItem(**dict(details))
                cart_item.save()
        return {}
