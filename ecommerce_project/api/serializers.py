from rest_framework import serializers
from cart.models import Product, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_price', 'quantity', 'total_price', 'added_at', 'user']

    def get_total_price(self, obj):
        return obj.total_price()

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exists")
        return value
    
class UpdateQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class CartTotalSerializer(serializers.Serializer):
    cart_total = serializers.DecimalField(decimal_places=2, max_digits=10)
    item_count = serializers.IntegerField()

