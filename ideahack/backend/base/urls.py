# backend/base/urls.py
from django.urls import path
from ideahack.backend.base.views import (
    LoginView,
    SignUpView,
    ChatView,
    ChatGPTView,
    Feed,
    CreateProject,
    MainPage,
    UserDetailView,
    ProjectDetailView,
    CompanyDetailView,
    InvestorDetailView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("chat/<str:user_type>/<int:id>/", ChatView.as_view(), name="chat-view"),
    path("chatgpt/<str:user_type>/<int:id>/", ChatGPTView.as_view(), name="chatgpt"),
    path("feed/", Feed.as_view(), name="feed-post"),
    path(
        "create-project/<str:user_type>/<int:id>/",
        CreateProject.as_view(),
        name="create-project",
    ),
    path("main/<str:user_type>/<int:id>/", MainPage.as_view(), name="main-page"),
    path("regular_user/<int:id>/", UserDetailView.as_view(), name="regular-user"),
    path("investor/<int:id>/", InvestorDetailView.as_view(), name="investor"),
    path("company/<int:id>/", CompanyDetailView.as_view(), name="company"),
    path("project/<int:id>/", ProjectDetailView.as_view(), name="project"),
]
