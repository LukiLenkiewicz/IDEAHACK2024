from openai import OpenAI
from google.oauth2 import service_account
from googleapiclient.discovery import build

API_KEY = "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"

class PitchDeckGenerator:
    def __init__(self, google_credentials_file):
        self.llm_client = OpenAI(api_key=API_KEY)
        self.google_credentials_file = google_credentials_file
        self.creds = service_account.Credentials.from_service_account_file(google_credentials_file, scopes=["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/drive"])
        self.slides_service = build('slides', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def generate_pitch_section(self, project_info, section_prompt: str):
        completion = self.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a venture capitalist creating a pitch deck for a new project. Your goal is to generate a compelling and brief project description. Response with max of 300 characters."},
                {"role": "user", "content": section_prompt.format(**project_info)}
            ],
            max_tokens=300,
        )
        response = completion.choices[0].message.content
        
        return response

    def generate_pitch_deck_content(self, project_info):
        sections = {
            "problem_statement": "Based on the following information: Project Bio: {bio} Area of Research: {area_of_research} Generate a compelling and brief project description suitable for a pitch-deck.",
            "solution_description": "Based on the following information: Project Name: {name} Project Bio: {bio} Area of Research: {area_of_research} Generate a compelling and brief project description suitable for a pitch-deck.",
            "investment_criteria": "Based on the cost structure of {cost_structure}, generate a brief investment criteria description including funding needs and expected returns.",
            "risk_description": "Provide a brief risk description for a project in the field of {area_of_research} with a focus on potential challenges.",
            "market_opportunity": "Generate a brief market analysis for the research area: {area_of_research}.",
            "competition_analysis": "Provide a brief overview of the competition in the field of {area_of_research}.",
            "confirmation_of_problem": "Briefly onfirm that the problem described in the project bio: {bio} exists, and provide sources if possible."
        }

        pitch_content = {}
        for section, prompt in sections.items():
            print(f"Generating content for {section}...")
            pitch_content[section] = self.generate_pitch_section(project_info, prompt)
        return pitch_content
    
    def create_presentation(self, title):
        body = {
            "title": title
        }
        presentation = self.slides_service.presentations().create(body=body).execute()
        # Set presentation to have public view rights
        self.set_public_view(presentation['presentationId'])
        return presentation['presentationId']
    
    def set_public_view(self, file_id):
        permission = {
            "type": "anyone",
            "role": "reader"
        }
        self.drive_service.permissions().create(fileId=file_id, body=permission).execute()

    def create_pitch_deck_presentation(self, pitch_content, presentation_id):
        requests = []

        slide_content_mappings = {
            "The Problem": "problem_statement",
            "Our Solution": "solution_description",
            "Market Opportunity": "market_opportunity",
            "Competition": "competition_analysis",
            "Investment Criteria": "investment_criteria",
            "Risks": "risk_description",
            "Confirmation of Problem Existence": "confirmation_of_problem",
        }

        slide_index = 1
        for slide_title, content_key in slide_content_mappings.items():
            requests.append({
                "createSlide": {
                    "objectId": f"slide_{content_key}",
                    "insertionIndex": slide_index,
                    "slideLayoutReference": {
                        "predefinedLayout": "TITLE_AND_BODY"
                    },
                    "placeholderIdMappings": [
                        {
                            "layoutPlaceholder": {
                                "type": "TITLE",
                                "index": 0
                            },
                            "objectId": f"{content_key}_title"
                        },
                        {
                            "layoutPlaceholder": {
                                "type": "BODY",
                                "index": 0
                            },
                            "objectId": f"{content_key}_text"
                        }
                    ]
                }
            })
            requests.append({
                "insertText": {
                    "objectId": f"{content_key}_title",
                    "text": slide_title,
                    "insertionIndex": 0
                }
            })
            requests.append({
                "insertText": {
                    "objectId": f"{content_key}_text",
                    "text": pitch_content.get(content_key, ""),
                    "insertionIndex": 0
                }
            })
            slide_index += 1

        body = {
            "requests": requests
        }

        response = self.slides_service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
        return response
    
    def get_presentation(self, presentation_id):
        presentation = self.slides_service.presentations().get(presentationId=presentation_id).execute()
        return presentation
    
    def generate_presentation_link(self, presentation_id):
        return f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    
    def download_presentation_as_pdf(self, presentation_id, output_filename):
        file_id = presentation_id
        request = self.drive_service.files().export(fileId=file_id, mimeType='application/pdf')
        with open(output_filename, 'wb') as pdf_file:
            response = request.execute()
            pdf_file.write(response)

    def generate_and_create_pitch_deck(self, project_info, presentation_title):
        pitch_content = self.generate_pitch_deck_content(project_info)
        presentation_id = self.create_presentation(presentation_title)
        self.create_pitch_deck_presentation(pitch_content, presentation_id)
        return presentation_id, pitch_content