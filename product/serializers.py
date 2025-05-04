from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product, Review, ProductImage
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id','image']
        
class ProductSerializers(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = CategorySerializer()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description','price','price_with_tax','stock','category','created_at','updated_at', 'images']
    
    def calculate_tax(self, product):   
        return round(product.price * Decimal(1.1), 2)
    
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price not less than 0.")
        return price 
    

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user','product','ratings','comment']
        read_only_fields = ['user', 'product']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.get_full_name()
        }

    def get_product(self, obj):
        return obj.product.name

    def create(self, validated_data):
        product_id = self.context['product_id']
        
        review = Review.objects.create(product_id=product_id, **validated_data)
        return review

