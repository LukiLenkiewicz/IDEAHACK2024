# backend/base/urls.py
from django.urls import path
from ideahack.backend.base.views import LoginView, SignUpView

urlpatterns = [
    path("api/signup/", SignUpView.as_view(), name="signup"),
    path("api/login/", LoginView.as_view(), name="login"),
]
