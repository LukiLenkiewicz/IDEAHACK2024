import os
import django
import random
from faker import Faker
from sentence_transformers import SentenceTransformer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ideahack.backend.backend.settings")
django.setup()
from ideahack.backend.base.models import User, Project, Company, Investor, Position
from ideahack.profile_store import ProfileStoreHandler
from ideahack.nls.vector_store import VectorStoreHandler
from ideahack.nls.search_engine import HybridSearchSystem
from ideahack.backend.backend.settings import BASE_DIR

from django.contrib.contenttypes.models import ContentType


# Set up Django


# Initialize Faker instance for generating random data
fake = Faker()
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
vector_store_handler = VectorStoreHandler(vector_store_file="vector_store.index")

profile_store_handler = ProfileStoreHandler(
    sentence_model=sentence_model, metadata_db_file=BASE_DIR / "db.sqlite3"
)


# Ensure skills is a list
def create_users(num=10):
    for _ in range(num):
        user = User.objects.create(
            name=fake.first_name(),
            surname=fake.last_name(),
            email=fake.email(),
            password=fake.password(),
            bio=fake.text(),
            experience=fake.text(),
            skills=fake.words(),
            link=fake.url(),
            type=random.choice(["Researcher", "Developer", "Engineer", "Doctor"]),
            keywords=fake.text(),
        )
        user_profile_data = {
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "bio": user.bio,
            "experience": user.experience,
            "skills": user.skills,
            "link": user.link,
            "type": user.type,
        }

        # If skills is a list of words, you can join them like this
        profile_store_handler.add_user_profile(user_profile_data, vector_store_handler)
        print(f"Created user: {user.name} {user.surname}")


# Generate some companies
def create_companies(num=5):
    for _ in range(num):
        company = Company.objects.create(
            name=fake.company(),
            email=fake.email(),
            password=fake.password(),
            bio=fake.text(),
            link=fake.url(),
            location=fake.address(),
            keywords=fake.text(),
            services=fake.text(),
        )
        company_profile_data = {
            "name": company.name,
            "email": company.email,
            "bio": company.bio,
            "services": company.services,
            "link": company.link,
            "location": company.location,
        }
        profile_store_handler.add_company_profile(
            company_profile_data, vector_store_handler
        )
        print(f"Created company: {company.name}")


# Generate some investors
def create_investors(num=5):
    for _ in range(num):
        investor = Investor.objects.create(
            name=fake.first_name(),
            email=fake.email(),
            password=fake.password(),
            bio=fake.text(),
            portfolio=fake.text(),
            interests=fake.text(),
            preferences=fake.text(),
            keywords=fake.text(),
        )
        print(f"Created investor: {investor.name}")


# Generate some projects
def create_projects(num=5):
    # Fetch content types for associations
    company_type = ContentType.objects.get_for_model(Company)
    investor_type = ContentType.objects.get_for_model(Investor)

    for _ in range(num):
        owner_type = random.choice([company_type, investor_type])
        owner = None
        if owner_type == company_type:
            owner = Company.objects.order_by("?").first()
        else:
            owner = Investor.objects.order_by("?").first()

        project = Project.objects.create(
            name=fake.bs(),
            bio=fake.text(),
            owner_type=owner_type.model,
            owner_id=owner.id,
            content_type=owner_type,
            requirements=fake.text(),
            email=fake.email(),
            pitch_deck=fake.text(),
            area_of_research=fake.text(),
            cost_structure=random.randint(1000, 10000),
            keywords=fake.text(),
        )
        print(f"Created project: {project.name}")


# Generate some positions
def create_positions(num=5):
    for _ in range(num):
        project = Project.objects.order_by("?").first()
        position = Position.objects.create(
            name=fake.job(),
            available=random.choice([True, False]),
            link=fake.url(),
            person_name=fake.first_name(),
            person_surname=fake.last_name(),
            project_id=project,
        )
        print(f"Created position: {position.name}")


# Main function to populate the database
def populate_database():
    create_users(10)
    create_companies(5)
    create_investors(5)
    create_projects(5)
    create_positions(5)


# Run the population function
if __name__ == "__main__":
    populate_database()
