# serializers.py
from rest_framework import serializers
from .models import User, Company, Investor


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "email", "password"]


class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = User
        fields = BaseSerializer.Meta.fields


class CompanySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Company
        fields = BaseSerializer.Meta.fields


class InvestorSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Investor
        fields = BaseSerializer.Meta.fields


def map_user_type(user_type):
    mapping = {
        "User": (User, UserSerializer),
        "Company": (Company, CompanySerializer),
        "Investor": (Investor, InvestorSerializer),
    }
    if user_type not in mapping:
        raise ValueError("Invalid user type")
    return mapping[user_type]