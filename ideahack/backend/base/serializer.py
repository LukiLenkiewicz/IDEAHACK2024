# serializers.py
from rest_framework import serializers
from .models import User, Company, Investor, Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = "__all__"


def map_user_type(user_type):
    mapping = {
        "User": (User, UserSerializer),
        "Company": (Company, CompanySerializer),
        "Investor": (Investor, InvestorSerializer),
    }
    if user_type not in mapping:
        raise ValueError("Invalid user type")
    return mapping[user_type]
