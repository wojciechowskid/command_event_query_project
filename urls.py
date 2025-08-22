from django.urls import path
from app1.views import create_user_view, get_user_view

urlpatterns = [
    path("create/", create_user_view),
    path("get/", get_user_view),
]

