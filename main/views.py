from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .models import BuyList
from .serializers import BuyListSerializer


def index_view(request):
    return render(request, 'index.html')


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("cabinet")
    return render(request, "login.html", context={'wrong_creds': True})


def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("cabinet")
    return render(request, "signup.html",)


def log_out(request):
    logout(request)
    return redirect("index")


class UserCabinetView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            redirect("index")

        lists = BuyList.objects.filter(user=request.user)
        return render(request, 'cabinet.html', context={'buy_lists': lists})


class BuyListAPIView(viewsets.ModelViewSet):
    serializer_class = BuyListSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return BuyList.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):

        # Add authorized user into data
        data = request.data
        sort_type = request.data.pop("sort_type")
        data['user'] = request.user.id

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            raise ValueError("Wrong format!")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True}, status=status.HTTP_201_CREATED, headers=headers)
