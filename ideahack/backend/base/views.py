from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django import forms
import uuid
from pydantic import BaseModel


from ideahack.backend.base.models import User, Project, Company, Investor
from ideahack.backend.base.serializer import map_user_type
from ideahack.backend.backend.settings import BASE_DIR
from ideahack.virtual_sibling.interact import VirtualSibling
from ideahack.profile_store import ProfileStoreHandler
from ideahack.nls.vector_store import VectorStoreHandler
from ideahack.nls.search_engine import HybridSearchSystem

from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
client = OpenAI()


class FormUser(BaseModel):
    name: str
    surname: str
    # "bio": str,
    # "experience": str,
    # "skills": str,
    # "link": str,
    # "type": str,


form = {
    "name": None,
    "surname": None,
    # "bio": None,
    # "experience": None,
    # "skills": None,
    # "link": None,
    # "type": None,
}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname"]


system_prompt = f"""
        You are a chatbot that helps users with creating their account. Use user's first 
        message to fill as much information as possible. After first answers 
        continue asking about not filled fields. Account is created when there are 
        no None values in form: {form}. At the end display whole form so user can verify 
        whether provided information is true or not. When form is filled say that they 
        can type 'quit' to exit.
        """

messages = [
    {"role": "system", "content": system_prompt},
]


class SignUpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = request.data.get("user_type")
        id = str(uuid.uuid4())

        request.data["id"] = id

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

            if user_type == "User":
                sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
                vector_store_handler = VectorStoreHandler(
                    vector_store_file="vector_store.index"
                )

                profile_store_handler = ProfileStoreHandler(
                    sentence_model=sentence_model,
                    metadata_db_file=BASE_DIR / "db.sqlite3",
                )
                user_profile_data = {
                    "name": "",
                    "surname": "",
                    "email": email,
                    "bio": "",
                    "experience": "",
                    "skills": "",
                    "link": "",
                    "type": "",
                }

                profile_store_handler.add_user_profile(
                    user_profile_data, vector_store_handler
                )
            if user_type == "Company":
                sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
                vector_store_handler = VectorStoreHandler(
                    vector_store_file="vector_store.index"
                )

                profile_store_handler = ProfileStoreHandler(
                    sentence_model=sentence_model,
                    metadata_db_file=BASE_DIR / "db.sqlite3",
                )
                company_profile_data = {
                    "name": "",
                    "email": email,
                    "bio": "",
                    "services": "",
                    "link": "",
                    "location": "",
                }
                profile_store_handler.add_company_profile(
                    company_profile_data, vector_store_handler
                )

            return Response(
                {
                    "email": user_instance.email,
                    "type": user_type,
                    "status": "success",
                },
                status=status.HTTP_200_OK,
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
        the_user = user_model.objects.get(email=email, password=password)
        if the_user is not None:
            return Response(
                {
                    "email": user_instance.email,
                    "type": user_type,
                    "status": "success",
                },
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


class ChatGPTView(APIView):
    def post(self, request, *args, **kwargs):
        # Initialize form with default values
        user_instance = User.objects.get(
            email="tmp@wp.pl"
        )  # Fetch the User instance by email
        print(user_instance)
        message = request.data["message"]

        messages.append({"role": "user", "content": message})
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini", messages=messages
        )
        chat_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": chat_message})

        if message.lower() == "quit":
            print("SIEMMMA")
            messages.append(
                {"role": "user", "content": "Display full filled form in .json format."}
            )
            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini", messages=messages, response_format=FormUser
            )
            filled_form = response.choices[0].message.content
            print(filled_form)
            user_instance = User.objects.get(
                email="tmp@wp.pl"
            )  # Fetch the User instance by email
            form = UserForm(filled_form, instance=user_instance)
            if form.is_valid():
                form.save()

            return Response(
                {
                    "message": chat_message,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": chat_message,
            },
            status=status.HTTP_200_OK,
        )


class Feed(APIView):
    def get(self, request):

        search_query = request.query_params.get('search_query', '')  # Default to empty string if not provided  # Get the query parameter
        # search_query = request.data.get("search_query")
        print(search_query)
        sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

        vector_store_handler = VectorStoreHandler(
            vector_store_file="vector_store.index"
        )

        profile_store_handler = ProfileStoreHandler(
            sentence_model=sentence_model, metadata_db_file=BASE_DIR / "db.sqlite3"
        )

        search_system = HybridSearchSystem(
            filters_file=BASE_DIR / "filters.json",
            vector_store_handler=vector_store_handler,
            profile_store_handler=profile_store_handler,
            sentence_model=sentence_model,
        )

        results = search_system.hybrid_search(search_query)

        return Response(
            {"message": "ok", "feed": results},
            status=status.HTTP_200_OK,
        )
