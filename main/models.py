from django.db import models
from django.contrib.auth.models import User


class BuyList(models.Model):
    title = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buylists_set')


class BuyItem(models.Model):
    title = models.CharField(max_length=255, blank=False)
    price = models.FloatField()
    quantity = models.IntegerField()
    buy_list = models.ForeignKey(BuyList, on_delete=models.CASCADE, related_name='items_set')
