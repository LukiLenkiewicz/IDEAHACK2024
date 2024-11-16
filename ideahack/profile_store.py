import sqlite3
import os
from sentence_transformers import SentenceTransformer
from ideahack.nls.vector_store import VectorStoreHandler

class ProfileStoreHandler:
    def __init__(self, sentence_model: SentenceTransformer, metadata_db_file='metadata.db'):
        # Initialize SQLite database for metadata
        self.sentence_model = sentence_model
        self.load_profiles_db(metadata_db_file)

    def load_profiles_db(self, metadata_db_file):
        if not os.path.exists(metadata_db_file):
            self.conn = sqlite3.connect(metadata_db_file)
            self.cursor = self.conn.cursor()

            # Create user_profiles table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS User (
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
            ''')
            # Create company_profiles table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Company (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    bio TEXT,
                    services TEXT,
                    link TEXT,
                    location TEXT,
                    vector_id INTEGER
                )
            ''')
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
        self.cursor.execute('''
            INSERT INTO User (name, surname, email, bio, experience, skills, link, type, vector_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (profile_data['name'], profile_data['surname'], profile_data['email'], profile_data['bio'], profile_data['experience'], ','.join(profile_data['skills']), profile_data['link'], profile_data['type'], vector_id))
        self.conn.commit()

    def add_company_profile(self, profile_data, vector_store_handler):
        vector_data = f"""
        {profile_data['bio']}
        
        {','.join(profile_data['services'])}
        """.strip()
        
        # Create vector from profile bio
        embedding = self.sentence_model.encode(vector_data, convert_to_tensor=False)
        # Add vector to vector store and get vector_id
        vector_id = vector_store_handler.add_vector(embedding)
        # Insert profile data into company_profiles table
        self.cursor.execute('''
            INSERT INTO Company (name, email, bio, services, link, location, vector_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (profile_data['name'], profile_data['email'], profile_data['bio'], ','.join(profile_data['services']), profile_data['link'], profile_data['location'], vector_id))
        self.conn.commit()

    def get_profile_by_vector_id(self, vector_id):
        
        for table, fields in [
            ('User', ['id', 'name', 'surname', 'email', 'bio', 'experience', 'skills', 'link', 'type', 'vector_id']),
            ('Company', ['id', 'name', 'email', 'bio', 'services', 'link', 'location', 'vector_id'])
        ]:
            self.cursor.execute(f'SELECT * FROM {table} WHERE vector_id = ?', (vector_id,))
            row = self.cursor.fetchone()
            if row:
                return {field: row[idx] for idx, field in enumerate(fields)}
        
        return None