from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_tags(self, obj):
        if float(obj.sale_price) >= 200:
            return 'Premium'
        return ''
