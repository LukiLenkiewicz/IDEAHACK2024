from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import uuid

from ideahack.backend.base.models import User, Project, Company, Investor
from ideahack.backend.base.serializer import map_user_type
from ideahack.backend.backend.settings import BASE_DIR
from ideahack.virtual_sibling.interact import VirtualSibling


class SignUpView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = request.data.get("user_type")
        id = str(uuid.uuid4())

        request.data["id"] = id

        if not all([name, email, password, user_type]):
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
                {"email": user_instance.email, "status": "success"},
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
                {"message": "Login successful", "email": user.email},
                status=status.HTTP_200_OK,
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
