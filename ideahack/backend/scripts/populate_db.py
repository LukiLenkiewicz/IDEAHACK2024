import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ideahack.backend.backend.settings")

# Initialize Django
django.setup()

from ideahack.backend.base.models import User, Project, Company, Investor
from ideahack.backend.backend.settings import BASE_DIR
import sqlite3


conn = sqlite3.connect(BASE_DIR / "db.sqlite3")
cursor = conn.cursor()


user = User.objects.create(
    id=1,
    name="John Doe",
    email="john.doe@example.com",
    password="hashed_password",
    description="Freelance software developer specializing in web applications.",
    experience="5 years of experience in full-stack development, worked on various projects for startups.",
    skills="Python, JavaScript, React, Node.js",
    website="https://johndoe.dev",
    social_media="https://linkedin.com/in/johndoe",
)

user = User.objects.create(
    id=6,
    name="Mikołaj Czachorowski",
    email="mikolaj@example.com",
    password="hashed_password",
    description="NLP enterprenuer, ML/AI filantrop, Chat gpt prompter.",
    experience="5 years of experience in prompt engineering, worked on various projects.",
    skills="Python, NLP, Prompt",
    website="https://github.com/Micz26",
    social_media="https://www.linkedin.com/in/mczachorowski/",
)

# Creating Project instance
project = Project.objects.create(
    id=1,  # Make sure ID is unique
    name="Project Alpha",
    description="A new web application to improve business processes.",
    field="Software Development",
    funds=50000,  # Example funding
    available_positions="Frontend Developer, Backend Developer",
)

# Creating Company instance
company = Company.objects.create(
    id=1,  # Make sure ID is unique
    name="Tech Solutions Inc.",
    email="contact@techsolutions.com",
    password="hashed_password",  # Use a hashed password in production (e.g., using Django's make_password)
    description="We specialize in AI-driven marketing solutions.",
    projects=project,  # Associate with the created project
)

# Creating Investor instance
investor = Investor.objects.create(
    id=1,  # Make sure ID is unique
    name="Jane Smith",
    email="jane.smith@example.com",
    password="hashed_password",  # Use a hashed password in production (e.g., using Django's make_password)
    description="Experienced investor in tech startups, focusing on AI and software solutions.",
)

user2 = User.objects.create(...)

user = User.objects.create(
    id=9,
    name="Lukasz Lenkiewicz",
    email="lukasz@example.com",
    password="hashed_password",
    description="NLP enterprenuer, ML/AI filantrop, Chat gpt prompter.",
    experience="5 years of experience in prompt engineering, worked on various projects.",
    skills="Python, NLP, Prompt",
    website="https://github.com/LukiLenkiewicz",
    social_media="https://www.linkedin.com/in/lukasz-lenkiewicz/",
)

print("Data has been populated successfully.")
