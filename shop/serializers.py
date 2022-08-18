from itertools import product
from rest_framework import serializers

from .models import Product, Category, Chat, Likelist, Watchlist, Rating


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance: Product):
        rep = super().to_representation(instance)
        rep["chats"] = ChatSerializer(instance.chat.all(), many=True).data
        rep["likes"] = instance.likes.all().count()
        rep["watches"] = instance.watches.all().count()
        rep["chatcount"] = instance.chat.all().count()
        rep["produrl"] = instance.get_absolute_url()
        rep["rating"] = instance.get_average_rating()

        return rep


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)
