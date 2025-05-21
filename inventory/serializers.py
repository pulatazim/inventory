from rest_framework import serializers


class ProductRequestSerializer(serializers.Serializer):
    product_code = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)