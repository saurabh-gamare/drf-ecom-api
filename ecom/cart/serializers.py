from rest_framework import serializers
from .models import Coupon, Cart, CartItem, Address


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    delivery_fee = serializers.IntegerField(read_only=True)
    total_payable = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.get('user')
        cart_details = Cart.objects.filter(user=user)
        if cart_details.exists():
            cart_details.update(**validated_data)
        else:
            cart = Cart(**validated_data)
            cart.save()
        cart_details = Cart.objects.get(user=user)
        return cart_details

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_payable'] = round(float(data['total_payable']), 2)
        data['coupon_discount'] = round(float(data['coupon_discount']), 2)
        data['total_mrp'] = round(float(data['total_mrp']), 2)
        data['total_sale_price'] = round(float(data['total_sale_price']), 2)
        return data


class CartProductDetailSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']


class CartItemSerializer(serializers.Serializer):
    cart_details = CartProductDetailSerializer(many=True)

    def create(self, validated_data):
        cart_instance = validated_data.get('cart_instance')
        cart_details = validated_data.get('cart_details')
        existing_cart_items = CartItem.objects.filter(user=cart_instance)
        existing_cart_products = [int(details.product_id) for details in existing_cart_items]
        new_cart_products = [int(details.get('product_id')) for details in cart_details]
        distinct_cart_products = list(set(existing_cart_products).symmetric_difference(set(new_cart_products)))
        for product_id in distinct_cart_products:
            cart_product = CartItem.objects.filter(user=cart_instance, product_id=product_id)
            if cart_product.exists():
                cart_product.delete()
            else:
                quantity = [details.get('quantity') for details in cart_details if
                            int(details.get('product_id')) == product_id] or [0]
                cart_item = CartItem(user=cart_instance, product_id=product_id, quantity=quantity[0])
                cart_item.save()
        for product_id in new_cart_products:
            if product_id in distinct_cart_products:
                continue
            cart_product = CartItem.objects.filter(user=cart_instance, product_id=product_id)
            quantity = [details.get('quantity') for details in cart_details if
                        details.get('product_id') == product_id] or [0]
            if cart_product.exists():
                cart_product.update(quantity=quantity[0])
        return {}


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def validate_address_label(self, value):
        address_instance = Address.objects.filter(address_label=value)
        if address_instance.exists():
            raise serializers.ValidationError(f'{value.capitalize()} address label already exists')
        return value
