from django.db import IntegrityError
from django.contrib.auth import authenticate, login


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from ideahack.backend.base.models import User, Project, Company, Investor
from ideahack.backend.base.serializer import map_user_type


class SignUpView(APIView):
    def post(self, request):
        # Extract user details from the request
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        password_2 = request.data.get("password_2")
        user_type = request.data.get("user_type")

        # Validate all fields are provided
        if not all([name, email, password, password_2, user_type]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Map user type to model and serializer
        try:
            model, serializer_class = map_user_type(user_type)
        except ValueError:
            return Response(
                {"error": "Invalid user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the email already exists across all models
        if any(
            m.objects.filter(email=email).exists() for m in [User, Company, Investor]
        ):
            return Response(
                {"error": "Email is already registered with another user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Use serializer for validation and creation
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
        # Extract email and password from the request
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = request.data.get("user_type")  # Expecting user_type to be specified

        # Validate required fields
        if not all([email, password, user_type]):
            return Response(
                {"error": "Email, password, and user type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate user type
        if user_type not in ["user", "company", "investor"]:
            return Response(
                {"error": "Invalid user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Determine the model based on user type
        user_model = {
            "user": User,
            "company": Company,
            "investor": Investor,
        }.get(user_type)

        # Try to find the user in the specified model
        try:
            user_instance = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Use Django's authentication system to verify credentials
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Log in the user and return a success response
            login(request, user)  # Creates a session
            return Response(
                {"message": "Login successful", "email": user.email},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
