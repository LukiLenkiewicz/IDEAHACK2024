# serializers.py
from rest_framework import serializers
from .models import User, Company, Investor


class BaseSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        fields = ["name", "surname", "email", "password", "password_2"]

    def validate(self, data):
        if data["password"] != data["password_2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = User
        fields = BaseSerializer.Meta.fields


class CompanySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Company
        fields = BaseSerializer.Meta.fields + ["company_name"]  # Example extra field


class InvestorSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Investor
        fields = BaseSerializer.Meta.fields + [
            "investment_focus"
        ]  # Example extra field


def map_user_type(user_type):
    mapping = {
        "user": (User, UserSerializer),
        "company": (Company, CompanySerializer),
        "investor": (Investor, InvestorSerializer),
    }
    if user_type not in mapping:
        raise ValueError("Invalid user type")
    return mapping[user_type]
