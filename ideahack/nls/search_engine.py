from openai import OpenAI
import json
from sentence_transformers import SentenceTransformer
from ideahack.nls.vector_store import VectorStoreHandler
from ideahack.profile_store import ProfileStoreHandler

API_KEY = "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"


class HybridSearchSystem:
    def __init__(
        self,
        filters_file: str,
        vector_store_handler: VectorStoreHandler,
        profile_store_handler: ProfileStoreHandler,
        sentence_model: SentenceTransformer,
    ):
        self.llm_client = OpenAI(api_key=API_KEY)

        self.vector_store_handler = vector_store_handler
        self.profile_store_handler = profile_store_handler
        self.sentence_model = sentence_model

        self.load_filters(filters_file)

    def load_filters(self, filters_file):
        with open(filters_file, "r") as f:
            self.filters = json.load(f)

    def parse_filters_and_classify_profiles(self, user_query):
        profile_types = self.filters.get("PROFILE_TYPES", [])
        filter_types = self.filters.get("FILTER_TYPES", {})
        filter_values = "\n".join(
            [f"{key}: {', '.join(values)}" for key, values in filter_types.items()]
        )

        system_prompt = f"""Your task is to classify profile types and extract filters based on user search query.
        Clssify what type of profiles the user is searching for into one or more of the following categories: {', '.join(profile_types)}.
        Extract filters for the following categories: {', '.join(filter_types)}.
        These filters can have the following possible values: 
        {filter_values}.
        Response only with the extracted filters and classified profile types."""

        completion = self.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
        )
        result = completion.choices[0].message.content

        print(f"\nResponse: {result}\n")

        # Extract profile types
        words = result.split()
        words = [word.strip(",.!?") for word in words]
        profiles = [word for word in words if word in profile_types]

        # Extract filters
        lines = result.split("\n")
        filters = {key: [] for key in filter_types}
        for line in lines:
            for key, values in filter_types.items():
                if key in line:
                    for value in values:
                        if value in line:
                            filters[key].append(value)

        return filters, profiles

    def filter_profiles(self, filters, profile_types):
        filtered_ids = []

        if "user" in profile_types:
            # Filter user profiles
            user_related_filters = {  # key - field in db, value - filter values
                "bio": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
                "experience": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
                "skills": filters.get("TECHNOLOGY", []),
                "type": filters.get("ROLE", []) + filters.get("INDUSTRY", []),
                "keywords": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
            }

            # select vector_id of users if any value in user_related_filters matches with the value in db in the respective field (key in user_related_filters)
            for field, values in user_related_filters.items():
                for value in values:
                    self.profile_store_handler.cursor.execute(
                        f"SELECT vector_id FROM base_user WHERE {field} LIKE ?",
                        (f"%{value}%",),
                    )
                    rows = self.profile_store_handler.cursor.fetchall()
                    filtered_ids.extend([row[0] for row in rows])

        if "company" in profile_types:
            # Filter company profiles
            company_related_filters = {  # key - field in db, value - filter values
                "bio": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
                "services": filters.get("TECHNOLOGY", []) + filters.get("INDUSTRY", []),
                "keywords": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
            }

            # select vector_id of companies if any value in company_related_filters matches with the value in db in the respective field (key in company_related_filters)
            for field, values in company_related_filters.items():
                for value in values:
                    self.profile_store_handler.cursor.execute(
                        f"SELECT vector_id FROM base_company WHERE {field} LIKE ?",
                        (f"%{value}%",),
                    )
                    rows = self.profile_store_handler.cursor.fetchall()
                    filtered_ids.extend([row[0] for row in rows])

        if "project" in profile_types:
            # Filter project profiles
            project_related_filters = {  # key - field in db, value - filter values
                "bio": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
                "requirements": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
                "area_of_research": filters.get("INDUSTRY", [])
                + filters.get("EXPERIENCE", []),
                "keywords": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
            }

            # select vector_id of projects if any value in project_related_filters matches with the value in db in the respective field (key in project_related_filters)
            for field, values in project_related_filters.items():
                for value in values:
                    self.profile_store_handler.cursor.execute(
                        f"SELECT vector_id FROM base_project WHERE {field} LIKE ?",
                        (f"%{value}%",),
                    )
                    rows = self.profile_store_handler.cursor.fetchall()
                    filtered_ids.extend([row[0] for row in rows])

        return list(set(filtered_ids))

    def hybrid_search(self, user_query):
        # Step 1: Parse the description into standard filters and classify intent
        filters, profile_types = self.parse_filters_and_classify_profiles(user_query)

        # Step 2: Filter the database of users and companies based on the filters
        filtered_ids = self.filter_profiles(filters, profile_types)

        # Step 3: Perform semantic search using the filtered FAISS index
        query_embedding = self.sentence_model.encode(
            user_query, convert_to_tensor=False
        )
        result_ids = self.vector_store_handler.search_vectors(
            query_embedding, filtered_ids, top_k=5
        )

        result_profiles = {"user": [], "company": [], "project": []}
        for res in result_ids:
            profile_type, profile = self.profile_store_handler.get_profile_by_vector_id(
                res["id"]
            )
            result_profiles[profile_type].append(profile)

        return result_profiles


class BasicFeedSystem:
    def __init__(
        self,
        profile_store_handler: ProfileStoreHandler,
        vector_store_handler: VectorStoreHandler,
        sentence_model: SentenceTransformer,
    ):
        self.profile_store_handler = profile_store_handler
        self.vector_store_handler = vector_store_handler
        self.sentence_model = sentence_model

    def get_user_profile(self, profile_id):
        self.profile_store_handler.cursor.execute(
            "SELECT * FROM base_user WHERE id = ?", (profile_id,)
        )
        row = self.profile_store_handler.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "bio": row[6],
                "experience": row[7],
                "skills": row[8],
                "vector_id": row[5],
                "type": row[10],
                "keywords": row[11],
            }
        return None

    def get_company_profile(self, profile_id):
        self.profile_store_handler.cursor.execute(
            "SELECT * FROM base_company WHERE id = ?", (profile_id,)
        )
        row = self.profile_store_handler.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "bio": row[5],
                "services": row[8],
                "vector_id": row[4],
            }
        return None

    def get_investor_profile(self, profile_id):
        self.profile_store_handler.cursor.execute(
            "SELECT * FROM base_investor WHERE id = ?", (profile_id,)
        )
        row = self.profile_store_handler.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "bio": row[4],
                "portfolio": row[5],
                "interests": row[6],
                "vector_id": None,  # Assuming investors don't have vector_id in the database
            }
        return None

    def get_project_profile(self, profile_id):
        self.profile_store_handler.cursor.execute(
            "SELECT * FROM base_project WHERE id = ?", (profile_id,)
        )
        row = self.profile_store_handler.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "bio": row[2],
                "requirements": row[7],
                "area_of_research": row[9],
                "vector_id": row[10],
            }
        return None

    def get_vector_ids_by_profile_type(self, profile_type):
        if profile_type == "user":
            self.profile_store_handler.cursor.execute(
                "SELECT vector_id FROM base_user WHERE vector_id IS NOT NULL"
            )
        elif profile_type == "company":
            self.profile_store_handler.cursor.execute(
                "SELECT vector_id FROM base_company WHERE vector_id IS NOT NULL"
            )
        elif profile_type == "project":
            self.profile_store_handler.cursor.execute(
                "SELECT vector_id FROM base_project WHERE vector_id IS NOT NULL"
            )
        else:
            return []

        rows = self.profile_store_handler.cursor.fetchall()
        return [row[0] for row in rows]

    def get_profile(self, profile_type, profile_id):
        if profile_type == "user":
            return self.get_user_profile(profile_id)
        elif profile_type == "company":
            return self.get_company_profile(profile_id)
        elif profile_type == "investor":
            return self.get_investor_profile(profile_id)
        elif profile_type == "project":
            return self.get_project_profile(profile_id)
        else:
            return None

    def get_profile_info(self, profile_type, profile):
        if profile_type == "user":
            profile_info = f"""
            {profile['bio']}
            {profile['experience']}
            {profile['skills']}
            {profile['type']}
            {profile['keywords']}
            """.strip()
        elif profile_type == "company":
            profile_info = f"""
            {profile['bio']}
            {profile['services']}
            {profile['keywords']}
            """.strip()
        elif profile_type == "investor":
            profile_info = f"""
            {profile['bio']}
            {profile['portfolio']}
            {profile['interests']}
            {profile['keywords']}
            {profile['preferences']}
            """.strip()
        elif profile_type == "project":
            profile_info = f"""
            {profile['bio']}
            {profile['requirements']}
            {profile['area_of_research']}
            {profile['keywords']}
            """.strip()
        return profile_info
    
    def search_similar_profiles(self, profile_type, profile_id):
        profile = self.get_profile(profile_type, profile_id)
        if not profile:
            return []

        # Generate embedding for the profile description
        profile_info = self.get_profile_info(profile_type, profile)
        profile_embedding = self.sentence_model.encode(
            profile_info, convert_to_tensor=False
        )

        # Determine which profile types to search for
        target_profile_types = []
        if profile_type == "user":
            target_profile_types = ["user", "project", "company"]
        elif profile_type == "company":
            target_profile_types = ["user", "project"]
        elif profile_type == "investor":
            target_profile_types = ["project", "company"]

        # Retrieve potential matches from the vector store
        similar_profiles = {}
        for target_type in target_profile_types:
            target_vector_ids = self.get_vector_ids_by_profile_type(target_type)
            if not target_vector_ids:
                continue
            if target_type == profile_type:
                target_vector_ids.remove(profile["vector_id"])
            
            # Perform vector similarity search
            result_ids = self.vector_store_handler.search_vectors(
                profile_embedding, target_vector_ids, top_k=20
            )

            similar_profiles[target_type] = [self.profile_store_handler.get_profile_by_vector_id(res["id"])[1] for res in result_ids]

        return similar_profiles
