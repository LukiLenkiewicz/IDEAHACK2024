# backend/base/urls.py
from django.urls import path
from ideahack.backend.base.views import (
    LoginView,
    SignUpView,
    ChatView,
    ChatGPTView,
    Feed,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("chat/<str:user_type>/<int:id>/", ChatView.as_view(), name="chat-view"),
    path("chatgpt/", ChatGPTView.as_view(), name="chatgpt"),
    path("feed/<str:user_type>/<str:id>/", Feed.as_view(), name="feed-post"),
]
