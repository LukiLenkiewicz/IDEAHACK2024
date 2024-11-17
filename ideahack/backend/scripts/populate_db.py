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


def create_quality_users():
    user = User.objects.create(
        name=fake.first_name(),
        surname=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
        bio="Python, nlp, developer, software developer, java, c++",
        experience="Python, nlp, developer, software developer, java, c++",
        skills="Python, nlp, developer, software developer, java, c++",
        link="https://github.com/LukiLenkiewicz",
        type=random.choice(["Researcher", "Developer", "Engineer", "Doctor"]),
        keywords="Python, nlp, developer, software developer, java, c++",
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
        "keywords": user.keywords,
    }

    # If skills is a list of words, you can join them like this
    profile_store_handler.add_user_profile(user_profile_data, vector_store_handler)
    print(f"Created user: {user.name} {user.surname}")

    user = User.objects.create(
        name="Mikołaj",
        surname="Czachorowski",
        email=fake.email(),
        password=fake.password(),
        bio="Mikołaj Czachorowski, a visionary entrepreneur, scientist, and self-made trillionaire under 20, is renowned for pioneering groundbreaking innovations in AI, quantum computing, and sustainable energy solutions. As the youngest tech mogul and founder of multiple industry-leading startups, Mikołaj has revolutionized how humanity interacts with technology. A recipient of the prestigious Nobel Prize in Physics and the youngest-ever member of the World Economic Forum, he is also an advocate for space exploration, bioengineering, and global philanthropic efforts aimed at eradicating poverty. With a passion for advancing humanity's future, Mikołaj is shaping the next era of scientific and technological progress.",
        experience="Founder & CEO of Quantum Horizons, a trillion-dollar AI & Quantum Computing startup revolutionizing industries. Lead scientist in pioneering sustainable fusion energy solutions. Investor and board member in over 50 breakthrough companies in AI, biotech, and clean energy. Nobel Laureate in Physics at 19 for contributions to quantum mechanics and quantum computing. Speaker at top global summits, including TED and the United Nations. Former CTO of SpaceX, helping to pioneer space commercialization.",
        skills="AI & Quantum Computing, Sustainable Energy, Space Exploration, Biotechnology, Leadership, Investment Strategies, Data Science, Machine Learning, Robotics, Blockchain, Strategic Innovation, Scientific Research, Philanthropy, Public Speaking, Advanced Programming (Python, C++, Java), Complex Problem Solving, Global Networking.",
        link="https://github.com/Micz26",
        type="Researcher",
        keywords="Entrepreneur, Scientist, Trillionaire, Innovator, Quantum Computing, AI, Sustainable Energy, Space Exploration, Nobel Prize, Bioengineering, Philanthropy, Tech Mogul, Visionary, Young Leader, Futurist, SpaceX, Data Science, Machine Learning, Blockchain.",
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
        "keywords": user.keywords,
    }

    # If skills is a list of words, you can join them like this
    profile_store_handler.add_user_profile(user_profile_data, vector_store_handler)
    print(f"Created user: {user.name} {user.surname}")

    user = User.objects.create(
        name="Tomasz",
        surname="Hałas",
        email=fake.email(),
        password=fake.password(),
        bio="Tomasz Hałas is an enthusiastic and motivated React.js intern, eager to learn and grow in the world of front-end development. As a self-taught programmer, Tomasz has a strong foundation in web development technologies and is currently focused on mastering React.js to build interactive and dynamic user interfaces. Passionate about coding and improving his skills, Tomasz is excited to gain real-world experience and contribute to innovative projects while continuously learning from more experienced developers.",
        experience="React.js Intern at Nokia, working on building responsive and interactive user interfaces. Currently learning best practices in React, JavaScript, HTML, and CSS. Contributing to small tasks in web development projects while gaining experience with React components, state management, and UI/UX principles. Actively collaborating with team members and seeking mentorship to expand knowledge in web development.",
        skills="React.js (basic knowledge), JavaScript, HTML, CSS, Git, Responsive Web Design, Problem Solving, Team Collaboration, Basic UI/UX principles, Agile Development, Web Development Fundamentals.",
        link="https://github.com/TomaszHalas",
        type="Intern",
        keywords="React.js, Intern, Front-End Development, Web Development, JavaScript, HTML, CSS, Beginner, Coding Enthusiast, Learning, Self-Taught, Team Collaboration, UI/UX, Web Design, Git.",
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
        "keywords": user.keywords,
    }

    # If skills is a list of words, you can join them like this
    profile_store_handler.add_user_profile(user_profile_data, vector_store_handler)
    print(f"Created user: {user.name} {user.surname}")

    user = User.objects.create(
        name="Jarosław",
        surname="Drapala",
        email=fake.email(),
        password=fake.password(),
        bio="Jarosław Drapala is a passionate and versatile researcher, focused on exploring innovative solutions in diverse fields such as artificial intelligence, renewable energy, and data science. With a keen interest in applying scientific principles to real-world challenges, Jarosław is committed to advancing human knowledge through interdisciplinary collaboration and cutting-edge research. His work is driven by a strong belief in the potential of technology to address some of the world's most pressing issues, including climate change, healthcare, and sustainability.",
        experience="Currently leading research projects in the fields of AI and machine learning, with a focus on creating practical, impactful applications. Previously worked as a research assistant in data science and computational modeling, contributing to peer-reviewed publications in high-impact journals. Collaborated with academic institutions and industry partners on several interdisciplinary projects that aim to solve complex societal problems. Regularly presents research at global conferences and actively contributes to the academic community through seminars and workshops.",
        skills="Research Methodology, Data Science, Machine Learning, AI Applications, Computational Modeling, Scientific Writing, Statistical Analysis, Data Visualization, Problem Solving, Interdisciplinary Collaboration, Research Project Management, Public Speaking, Peer Review, Scientific Publishing.",
        link="https://github.com/JaroslawDrapala",
        type="Researcher",
        keywords="Researcher, Artificial Intelligence, Machine Learning, Data Science, Renewable Energy, Sustainability, Climate Change, Healthcare Innovation, Computational Modeling, Scientific Writing, Innovation, Interdisciplinary Collaboration, Technology for Good.",
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
        "keywords": user.keywords,
    }

    # If skills is a list of words, you can join them like this
    profile_store_handler.add_user_profile(user_profile_data, vector_store_handler)
    print(f"Created user: {user.name} {user.surname}")


# Ensure skills is a list
def create_users(num=10):
    create_quality_users()
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
            "keywords": user.keywords,
        }

        # If skills is a list of words, you can join them like this
        profile_store_handler.add_user_profile(user_profile_data, vector_store_handler)
        print(f"Created user: {user.name} {user.surname}")


def create_quality_companies():
    company = Company.objects.create(
        name="Nokia",
        email="contact@nokia.com",
        password=fake.password(),  # You can replace with actual password if needed
        bio="Nokia is a global leader in the telecommunications and technology industry, providing innovative solutions in 5G, IoT, and network infrastructure. With a rich history of shaping the future of mobile communications, Nokia continues to drive the evolution of mobile networks, connectivity, and digital transformation for businesses and consumers worldwide. Nokia's commitment to sustainability, security, and connectivity ensures that it remains a cornerstone of the tech world.",
        link="https://www.nokia.com",
        location="Espoo, Finland",
        keywords="telecommunications, 5G, IoT, network infrastructure, mobile networks, connectivity, sustainability, technology, global leader",
        services="Telecommunications Solutions, 5G Infrastructure, Internet of Things (IoT), Mobile Networks, Digital Transformation, Network Security, Software Solutions, Enterprise Services, Smart Cities Solutions.",
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
    # NeuralSpie Profile (Embedded AI Startup)
    company = Company.objects.create(
        name="NeuralSpike",
        email="info@neuralspie.com",
        password=fake.password(),  # You can replace with actual password if needed
        bio="NeuralSpie is a cutting-edge embedded AI startup focused on integrating artificial intelligence into everyday devices. By creating highly efficient, low-power AI solutions, NeuralSpie aims to revolutionize industries ranging from automotive to consumer electronics. Their embedded AI technology empowers products with enhanced decision-making capabilities, adaptive behaviors, and real-time data processing, making it possible to create smarter, more intuitive devices. NeuralSpie is at the forefront of the AI revolution, enabling seamless integration of intelligence into the hardware ecosystem.",
        link="https://www.neuralspie.com",
        location="San Francisco, California, USA",
        keywords="embedded AI, artificial intelligence, low-power AI, real-time data processing, smart devices, automotive AI, consumer electronics, startup, AI technology",
        services="Embedded AI Solutions, AI Hardware Integration, Edge AI, Real-Time Data Processing, Machine Learning for Embedded Systems, Smart Device Development, Automotive AI, Consumer Electronics AI.",
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
    # Hypersqurek Profile
    company = Company.objects.create(
        name="Hypersqurek",
        email="contact@hypersqurek.com",
        password=fake.password(),  # You can replace with actual password if needed
        bio="Hypersqurek is an innovative tech company specializing in advanced quantum computing solutions and hyper-advanced software systems. At the cutting edge of computational power, Hypersqurek is dedicated to creating quantum solutions that push the limits of technology, providing businesses with breakthrough capabilities in data analysis, cryptography, and computational modeling. Their goal is to empower industries such as finance, pharmaceuticals, and aerospace with the next-generation computing solutions required to solve the world's most complex problems.",
        link="https://www.hypersqurek.com",
        location="Zurich, Switzerland",
        keywords="quantum computing, data analysis, cryptography, software systems, computational modeling, advanced technology, finance, pharmaceuticals, aerospace, industry solutions",
        services="Quantum Computing Solutions, Data Analysis & Modeling, Cryptography & Security, Software Development for Quantum Systems, Computational Problem Solving, Industry-Specific Quantum Solutions (Finance, Pharma, Aerospace).",
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


# Generate some companies
def create_companies(num=5):
    create_quality_companies()
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
        
        project_profile_data = {
            "name": project.name,
            "bio": project.bio,
            "owner_type": project.owner_type,
            "owner_id": project.owner_id,
            "requirements": project.requirements,
            "email": project.email,
            "pitch_deck": project.pitch_deck,
            "area_of_research": project.area_of_research,
            "cost_structure": project.cost_structure,
            "keywords": project.keywords,
        }
        profile_store_handler.add_project_profile(
            project_profile_data, vector_store_handler
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
