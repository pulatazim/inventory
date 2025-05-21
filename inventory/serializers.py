from rest_framework import serializers


class ProductRequestSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)