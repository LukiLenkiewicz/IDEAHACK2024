import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ideahack.backend.backend.settings")

# Initialize Django
django.setup()

from ideahack.backend.base.models import User, Project, Company, Investor
import sqlite3


# Connect to your SQLite database
conn = sqlite3.connect(
    r"C:\\Users\\mikol\\PythonProjects\\IDEAHACK2024\\ideahack\\backend\\db.sqlite3"
)
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

# Example of adding more users or modifying data if needed
# user2 = User.objects.create(...)

print("Data has been populated successfully.")
