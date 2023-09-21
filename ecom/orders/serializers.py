from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Address
from products.models import Product
from django.db.models import F


class OrderSerializer(serializers.ModelSerializer):
    address_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['address_id']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['id', 'user', 'address_label']


class RetrieveOrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    customer_details = CustomerDetailSerializer(source='address', read_only=True)
    item_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_status(self, obj):
        status_choices = Order.STATUS_FIELD_CHOICES
        return [details[1] for details in status_choices if details[0] == obj.status][0]

    def get_item_details(self, obj):
        instance = ((OrderItem.objects.select_related('product_id', 'order')
                     .filter(order_id__order_id=obj.order_id))
                    .values('quantity', 'product_id',
                            product_image=F('product_id__product_image'),
                            size=F('product_id__size'),
                            total_mrp=F('product_id__mrp')*F('quantity'),
                            product_name=F('product_id__product_name'),
                            # total_sale_price=F('product_id__sale_price')*F('quantity')
                            ))
        for details in instance:
            product_instance = Product.objects.get(id=details.get('product_id'))
            details['total_sale_price'] = round(float(product_instance.sale_price) * float(details.get('quantity')), 2)
        return instance


class ListOrderSerializer(serializers.ModelSerializer):
    product_names = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'created_on', 'total_payable', 'status', 'product_names']

    def get_product_names(self, obj):
        instance = ((OrderItem.objects.select_related('product_id', 'order')
                     .filter(order_id__order_id=obj.order_id))
                    .values('product_id__product_name'))
        return ', '.join([details.get('product_id__product_name') for details in instance])

    def get_status(self, obj):
        status_choices = Order.STATUS_FIELD_CHOICES
        return [details[1] for details in status_choices if details[0] == obj.status][0]
