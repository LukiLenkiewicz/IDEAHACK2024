from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

import uuid

from ideahack.backend.base.models import User, Project, Company, Investor
from ideahack.backend.base.serializer import map_user_type
from ideahack.backend.backend.settings import BASE_DIR
from ideahack.virtual_sibling.interact import VirtualSibling


class SignUpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = request.data.get("user_type")
        id = str(uuid.uuid4())

        request.data["id"] = id
        print(request.data)

        if not all([email, password, user_type]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            model, serializer_class = map_user_type(user_type)
        except ValueError:
            return Response(
                {"error": "Invalid user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if any(
            m.objects.filter(email=email).exists() for m in [User, Company, Investor]
        ):
            return Response(
                {"error": "Email is already registered with another user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data.pop("user_type", None)

        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user_instance = serializer.save()

            return Response(
                {
                    "email": user_instance.email,
                    "type": user_type,
                    "status": "success",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = request.data.get("user_type")

        if not all([email, password, user_type]):
            return Response(
                {"error": "Email, password, and user type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_type not in ["user", "company", "investor"]:
            return Response(
                {"error": "Invalid user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_model = {
            "user": User,
            "company": Company,
            "investor": Investor,
        }.get(user_type)

        try:
            user_instance = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {
                    "email": user_instance.email,
                    "type": user_type,
                    "status": "success",
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChatView(APIView):
    def post(self, request, user_type, id):
        # Log the incoming data for debugging
        print(f"Received data: {request.data}")  # Debug line

        # Ensure `request.data` is not empty and contains the expected field
        user_query = request.data.get("query")

        if not user_query:
            return Response(
                {"error": "Query parameter is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(user_query)

        virtual_sibling = VirtualSibling(
            profile_id=id,
            profile_type=user_type,
            db_path=BASE_DIR / "db.sqlite3",
        )

        answer = virtual_sibling.query(user_query=user_query)

        print(answer)
        return Response(
            {"message": "ok", "answer": answer},
            status=status.HTTP_200_OK,
        )


class Settings(APIView):
    def post(self, request, user_type, id):
        if user_type == "user":
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )

            description = request.data.get("description", user.description)
            experience = request.data.get("experience", user.experience)
            skills = request.data.get("skills", user.skills)
            website = request.data.get("website", user.website)
            social_media = request.data.get("social_media", user.social_media)

            user.description = description
            user.experience = experience
            user.skills = skills
            user.website = website
            user.social_media = social_media
            user.save()

            return Response(
                {"message": "User settings updated successfully."},
                status=status.HTTP_200_OK,
            )

        elif user_type == "company":
            try:
                company = Company.objects.get(id=id)
            except Company.DoesNotExist:
                return Response(
                    {"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND
                )

            description = request.data.get("description", company.description)

            company.description = description
            company.save()

            return Response(
                {"message": "Company settings updated successfully."},
                status=status.HTTP_200_OK,
            )

        elif user_type == "investor":
            try:
                investor = Investor.objects.get(id=id)
            except Investor.DoesNotExist:
                return Response(
                    {"error": "Investor not found."}, status=status.HTTP_404_NOT_FOUND
                )

            description = request.data.get("description", investor.description)

            investor.description = description
            investor.save()

            return Response(
                {"message": "Investor settings updated successfully."},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST
            )
