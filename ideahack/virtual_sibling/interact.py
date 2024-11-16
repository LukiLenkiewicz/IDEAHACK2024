import sqlite3
from openai import OpenAI
import json
from scrapegraphai.graphs import SmartScraperGraph

API_KEY = "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"


class VirtualSibling:
    def __init__(self, profile_id, profile_type, db_path):
        self.profile_id = profile_id
        self.profile_type = profile_type
        self.profile_data: dict = json.loads(self._get_profile_data(db_path))
        self.llm_client = OpenAI(api_key=API_KEY)
        self._init_predefined_responses()

        self.greet_user()

    def _get_profile_data(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if self.profile_type == "user":
            cursor.execute(
                """SELECT name, surname, bio, experience, skills, link, type, keywords FROM base_user WHERE id = ?""",
                (self.profile_id,),
            )
        elif self.profile_type == "company":
            cursor.execute(
                """SELECT name, bio, link, location, keywords, services FROM base_company WHERE id = ?""",
                (self.profile_id,),
            )

        profile_data = cursor.fetchone()
        conn.close()

        if profile_data:
            keys = (
                [
                    "name",
                    "surname",
                    "bio",
                    "experience",
                    "skills",
                    "link",
                    "type",
                    "keywords",
                ]
                if self.profile_type == "user"
                else ["name", "bio", "link", "location", "keywords", "services"]
            )
            return json.dumps(dict(zip(keys, profile_data)), indent=4)
        else:
            raise ValueError("Profile not found.")

    def _init_predefined_responses(self):
        self.responses = {
            "greeting": f"Hello! I'm a virtual sibling of {self.profile_data['name']}. Tell me what do you want to know about me?",
            "info_not_found": "Unfortunately, I don't have enough information to answer that.",
        }

    def greet_user(self):
        print(self.responses["greeting"])

    def _chat_with_website(self, url, user_query):
        graph_config = {
            "llm": {
                "api_key": API_KEY,
                "model": "openai/gpt-4o-mini",
            },
            "verbose": False,
            "headless": True,
        }

        scraper = SmartScraperGraph(
            prompt=f"""Find information sufficient to answer the user's question. Provide answer in plain text. If insufficient, respond with, '{self.responses['info_not_found']}''
            
            User question: {user_query}""",
            source=url,
            config=graph_config,
        )

        answer = scraper.run()
        return answer

    def query(self, user_query):
        # Extract profile information
        name, description = self.profile_data["name"], self.profile_data["bio"]
        details = [
            self.profile_data[key]
            for key in self.profile_data
            if key not in ["name", "bio"]
        ]

        profile_info = (
            f"Name: {name}\nDescription: {description}\nDetails: {'; '.join(details)}"
        )

        # Construct system prompt for language model
        system_prompt = f"""Profile Information:
        {profile_info}
        
        Instructions: Answer strictly based only on the above information. If insufficient, respond with, '{self.responses['info_not_found']}'."""

        # Call OpenAI API (assuming API key is set)
        completion = self.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
        )

        answer = completion.choices[0].message.content

        answer = self.responses["info_not_found"]

        if self.responses["info_not_found"] in answer:
            # Scrape website for additional information
            website = self.profile_data["link"]

            if website:  # If website info was provided
                answer = list(self._chat_with_website(website, user_query).values())[0]

                if answer.strip() == "NA":
                    answer = self.responses["info_not_found"]

        return answer
