from pickle import FALSE
from sqlite3 import Date
from tokenize import Name
from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ideahack.backend.base.models import (
    Engineer,
    Researcher,
    Project,
    ResearchCenterRepresentative,
    CompanyRepresentative,
)
from ideahack.backend.backend_utils.views_utils import map_user_type


class RegisterView(APIView):
    def post(self, request):
        name = request.data.get("name")
        surname = request.data.get("surname")
        user_type = request.data.get("user_type")
        email = request.data.get("email")
        password = request.data.get("password")
        password_2 = request.data.get("password_2")

        if not all([name, surname, user_type, email, password, password_2]):
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if password != password_2:
            return Response(
                {"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
            )

        if any(
            model.objects.filter(email=email).exists()
            for model in [
                Researcher,
                Engineer,
                ResearchCenterRepresentative,
                CompanyRepresentative,
            ]
        ):
            return Response(
                {"error": "Email is already registered with another user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_model = map_user_type(user_type)
        except ValueError:
            return Response(
                {"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_instance = user_model.objects.create(
                name=name,
                surname=surname,
                email=email,
                # Add additional fields like bio, location, etc., or leave them as empty strings
                bio="",
                profileimg=None,  # You might want to handle the profile image field
                location="",
                work_expirience="",
                research_papers="",
                projects="",
                linkedin="",
                github="",
                google_scholar="",
                other_urls="",
            )

            # Optionally, if password handling is external, create a password field or a token here

            # Return a success response
            return Response(
                {"email": user_instance.email, "status": "success"},
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError as e:
            # Handle any database integrity errors (e.g., duplicate entry or missing required fields)
            return Response(
                {"error": "Database error, please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            # Handle any unforeseen errors (e.g., server issues)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        return Response(
            {"email": email, "status": "success"}, status=status.HTTP_200_OK
        )
