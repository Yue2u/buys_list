from rest_framework import serializers

from .models import BuyList, BuyItem


class BuyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyItem
        fields = ('title', 'price', 'quantity')


class BuyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyList
        fields = ('title', 'user', 'items_set')

    items_set = BuyItemSerializer(many=True, required=False)

    def create(self, validated_data):
        items_set = validated_data.pop("items_set")
        buy_list = BuyList.objects.create(**validated_data)
        for item in items_set:
            BuyItem.objects.create(buy_list=buy_list, **item)

        return buy_list
