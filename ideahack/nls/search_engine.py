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

        if "USER" in profile_types:
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
            }
            print(user_related_filters)

            # select vector_id of users if any value in user_related_filters matches with the value in db in the respective field (key in user_related_filters)
            for field, values in user_related_filters.items():
                for value in values:
                    self.profile_store_handler.cursor.execute(
                        f"SELECT vector_id FROM base_user WHERE {field} LIKE ?",
                        (f"%{value}%",),
                    )
                    rows = self.profile_store_handler.cursor.fetchall()
                    filtered_ids.extend([row[0] for row in rows])
                    for row in rows:
                        print(row)

        if "COMPANY" in profile_types:
            # Filter company profiles
            company_related_filters = {  # key - field in db, value - filter values
                "bio": filters.get("TECHNOLOGY", [])
                + filters.get("INDUSTRY", [])
                + filters.get("ROLE", [])
                + filters.get("EXPERIENCE", []),
                "services": filters.get("TECHNOLOGY", []) + filters.get("INDUSTRY", []),
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

        result_profiles = []
        for res in result_ids:
            profile = self.profile_store_handler.get_profile_by_vector_id(res["id"])
            result_profiles.append(profile)
            print(profile)

        return result_profiles
