import sqlite3
import os
from sentence_transformers import SentenceTransformer

from ideahack.nls.vector_store import VectorStoreHandler
from ideahack.backend.backend.settings import BASE_DIR


class ProfileStoreHandler:
    def __init__(
        self,
        sentence_model: SentenceTransformer,
        metadata_db_file=BASE_DIR / "db.sqlite3",
    ):
        # Initialize SQLite database for metadata
        self.sentence_model = sentence_model
        self.load_profiles_db(metadata_db_file)

    def load_profiles_db(self, metadata_db_file):
        if not os.path.exists(metadata_db_file):
            self.conn = sqlite3.connect(metadata_db_file)
            self.cursor = self.conn.cursor()

            # Create user_profiles table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS base_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email TEXT,
                    bio TEXT,
                    experience TEXT,
                    skills TEXT,
                    link TEXT,
                    type TEXT,
                    vector_id INTEGER
                )
            """)
            # Create company_profiles table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS base_company (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    bio TEXT,
                    services TEXT,
                    link TEXT,
                    location TEXT,
                    vector_id INTEGER
                )
            """)
            self.conn.commit()
        else:
            self.conn = sqlite3.connect(metadata_db_file)
            self.cursor = self.conn.cursor()

    def add_user_profile(self, profile_data, vector_store_handler: VectorStoreHandler):
        vector_data = f"""
        {profile_data['bio']}
        
        {profile_data['experience']}
        
        {','.join(profile_data['skills'])}
        
        {profile_data['type']}
        """.strip()

        # Create vector from profile bio
        embedding = self.sentence_model.encode(vector_data, convert_to_tensor=False)
        # Add vector to vector store and get vector_id
        vector_id = vector_store_handler.add_vector(embedding)
        # Insert profile data into user_profiles table
        self.cursor.execute(
            """
            SELECT id FROM base_user WHERE email = ?
            """,
            (profile_data["email"],),
        )

        # Fetch the result of the query (user_id)
        user = self.cursor.fetchone()

        # Check if the user exists
        if user:
            user_id = user[0]  # The ID of the user found

            # Update the user with the vector_id
            self.cursor.execute(
                """
                UPDATE base_user 
                SET vector_id = ? 
                WHERE id = ?
                """,
                (vector_id, user_id),
            )
            self.conn.commit()
            print(f"User with email {profile_data['email']} updated with vector_id.")
        else:
            print(f"User with email {profile_data['email']} not found.")

    def add_company_profile(self, profile_data, vector_store_handler):
        vector_data = f"""
        {profile_data['bio']}
        
        {','.join(profile_data['services'])}
        """.strip()

        # Create vector from profile bio
        embedding = self.sentence_model.encode(vector_data, convert_to_tensor=False)
        # Add vector to vector store and get vector_id
        vector_id = vector_store_handler.add_vector(embedding)

        # Fetch the company by email
        self.cursor.execute(
            """
            SELECT id FROM base_company WHERE email = ?
            """,
            (profile_data["email"],),
        )

        # Fetch the result of the query (company_id)
        company = self.cursor.fetchone()

        # Check if the company exists
        if company:
            company_id = company[0]  # The ID of the company found

            # Update the company with the new vector_id
            self.cursor.execute(
                """
                UPDATE base_company 
                SET vector_id = ? 
                WHERE id = ?
                """,
                (vector_id, company_id),
            )
            self.conn.commit()
            print(f"Company with email {profile_data['email']} updated with vector_id.")
        else:
            print(f"Company with email {profile_data['email']} not found.")

    def get_profile_by_vector_id(self, vector_id):
        row_id = 0
        for table, fields in [
            (
                "base_user",
                [
                    "id",
                    "name",
                    "bio",
                ],
            ),
            (
                "base_company",
                [
                    "id",
                    "name",
                    "bio",
                ],
            ),
            (
                "base_project",
                [
                    "id",
                    "name",
                    "bio",
                ],
            ),
        ]:
            row_id += 1
            self.cursor.execute(
                f"SELECT id, name, bio FROM {table} WHERE vector_id = ?", (vector_id,)
            )
            row = self.cursor.fetchone()
            if row:
                profile_type = "USER" if table == "base_user" else "COMPANY" if table == "base_company" else "PROJECT"
                return (profile_type, {field: row[idx] for idx, field in enumerate(fields)} | {
                    "rowID": row_id
                })

        return None
