from typing import Union
import json
from openai import OpenAI
from dotenv import load_dotenv

from ideahack.recommendations.models import ListPeople
from ideahack.recommendations.prompts import get_summary_prompt, get_user_prompt


client = OpenAI()

with open("./data/toy_user_data.json", 'r') as file:
    data = json.load(file)


def recommend_person(project_description: Union[str, dict]) -> ListPeople:
    user_prompt = get_user_prompt(project_description)

    output = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": get_summary_prompt(data)},
            {"role": "user","content": user_prompt}],
            response_format=ListPeople
        )
    
    return output.choices[0].message.parsed.people
