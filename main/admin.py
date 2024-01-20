from django.contrib import admin

from .models import BuyList, BuyItem


admin.site.register(BuyList)
admin.site.register(BuyItem)
