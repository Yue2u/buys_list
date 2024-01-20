from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import index_view, UserCabinetView, log_in, sign_up, log_out, BuyListAPIView

router = DefaultRouter()
router.register(r"api/buys_list", BuyListAPIView, basename='buys-list')

urlpatterns = [
    path('', index_view, name='index'),
    path('', include(router.urls)),
    path('cabinet/', UserCabinetView.as_view(), name='cabinet'),
    path('login/', log_in, name='login'),
    path('login/', sign_up, name='signup'),
    path('logout/', log_out, name='logout')
]
