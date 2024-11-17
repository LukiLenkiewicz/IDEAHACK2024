import ast

from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django import forms
import uuid
from pydantic import BaseModel


from ideahack.backend.base.models import User, Project, Company, Investor
from ideahack.backend.base.serializer import (
    map_user_type,
    UserSerializer,
    CompanySerializer,
    ProjectSerializer,
    InvestorSerializer,
)
from ideahack.backend.backend.settings import BASE_DIR
from ideahack.virtual_sibling.interact import VirtualSibling
from ideahack.profile_store import ProfileStoreHandler
from ideahack.nls.vector_store import VectorStoreHandler
from ideahack.nls.search_engine import HybridSearchSystem, BasicFeedSystem


from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
client = OpenAI()


class FormUser(BaseModel):
    name: str
    surname: str
    bio: str
    experience: str
    skills: str
    link: str
    type: str


form = {
    "name": None,
    "surname": None,
    "bio": None,
    "experience": None,
    "skills": None,
    "link": None,
    "type": None,
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
                    "id": id,
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
        if user_type not in ["User", "Company", "Investor"]:
            return Response(
                {"error": "Invalid user type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model_dict = {
            "user": User,
            "company": Company,
            "investor": Investor,
        }
        user_model = model_dict[user_type.lower()]

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
                    "id": id,
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
        print(f"Received data: {request.data}")  # Debugging

        user_query = request.data.get("query")
        if not user_query:
            return Response(
                {"error": "Query parameter is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            virtual_sibling = VirtualSibling(
                profile_id=id,
                profile_type=user_type,
                db_path=BASE_DIR / "db.sqlite3",
            )
            answer = virtual_sibling.query(user_query=user_query)
            print(answer)
            return Response(
                {"message": "ok", "answer": answer, "id": id},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:  # Handle missing profile or invalid ID
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:  # Catch other unexpected errors
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ChatGPTView(APIView):
    def post(self, request, user_type, id):
        model_dict = {
            "user": User,
            "company": Company,
            "investor": Investor,
        }
        user_model = model_dict[user_type.lower()]
        user_instance = user_model.objects.get(id=id)
        print(user_instance)
        message = request.data.get("messages")

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
            filled_form = ast.literal_eval(filled_form)
            user_instance = User.objects.get(email=user_instance.email)
            form = UserForm(filled_form, instance=user_instance)
            if form.is_valid():
                form.save()

            return Response(
                {"message": chat_message, "id": id},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": chat_message, "id": id},
            status=status.HTTP_200_OK,
        )


class Feed(APIView):
    def get(self, request):
        search_query = request.query_params.get(
            "search_query", ""
        )  # Default to empty string if not provided  # Get the query parameter
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
            {"message": "ok", "feed": results, "id": id},
            status=status.HTTP_200_OK,
        )


class CreateProject(APIView):
    def post(self, request, user_type, id):
        data = request.data

        required_fields = [
            "name",
            "bio",
            "requirements",
            "email",
            "area_of_research",
            "cost_structure",
            "keywords",
        ]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        owner_model_map = {
            "user": User,
            "company": Company,
            "investor": Investor,
        }

        owner_model = owner_model_map.get(user_type.lower())
        if not owner_model:
            return Response(
                {
                    "error": f"Invalid user_type. Must be one of {', '.join(owner_model_map.keys())}."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            owner = owner_model.objects.get(id=id)
        except owner_model.DoesNotExist:
            return Response(
                {"error": f"Owner with id {id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        content_type = ContentType.objects.get_for_model(owner)

        try:
            project = Project.objects.create(
                name=data.get("name"),
                bio=data.get("bio"),
                owner_type=user_type.lower(),
                owner_id=owner.id,
                content_type=content_type,
                requirements=data.get("requirements"),
                email=data.get("email"),
                pitch_deck=data.get("pitch_deck", ""),
                area_of_research=data.get("area_of_research", ""),
                cost_structure=data.get("cost_structure", 0),
                keywords=data.get("keywords", ""),
                vector_id=data.get("vector_id", None),
            )
            return Response(
                {
                    "message": "Project created successfully.",
                    "project": {
                        "id": project.id,
                        "name": project.name,
                        "bio": project.bio,
                        "owner_type": project.owner_type,
                        "email": project.email,
                        "requirements": project.requirements,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create project: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MainPage(APIView):
    def get(self, request, user_type, id):
        sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

        vector_store_handler = VectorStoreHandler(
            vector_store_file="vector_store.index"
        )

        profile_store_handler = ProfileStoreHandler(
            sentence_model=sentence_model, metadata_db_file=BASE_DIR / "db.sqlite3"
        )

        search_system = BasicFeedSystem(
            vector_store_handler=vector_store_handler,
            profile_store_handler=profile_store_handler,
            sentence_model=sentence_model,
        )

        results = search_system.search_similar_profiles(user_type, id)

        return Response(
            {"message": "ok", "feed": results, "id": id},
            status=status.HTTP_200_OK,
        )


class UserDetailView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=404)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)


# View for Company model
class CompanyDetailView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                company = Company.objects.get(id=id)
                serializer = CompanySerializer(company)
                return Response(serializer.data)
            except Company.DoesNotExist:
                return Response({"error": "Company not found."}, status=404)
        else:
            companies = Company.objects.all()
            serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data)


# View for Project model
class ProjectDetailView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                project = Project.objects.get(id=id)
                serializer = ProjectSerializer(project)
                return Response(serializer.data)
            except Project.DoesNotExist:
                return Response({"error": "Project not found."}, status=404)
        else:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)


# View for Investor model
class InvestorDetailView(APIView):
    def get(self, request, id):
        if id:
            try:
                investor = Investor.objects.get(id=id)
                serializer = InvestorSerializer(investor)
                return Response(serializer.data)
            except Investor.DoesNotExist:
                return Response({"error": "Investor not found."}, status=404)
        else:
            investors = Investor.objects.all()
            serializer = InvestorSerializer(investors, many=True)
            return Response(serializer.data)
