from typing import Union
import json
from openai import OpenAI
from dotenv import load_dotenv

from ideahack.recommendations.models import ListPeople
from ideahack.recommendations.prompts import get_user_prompt_for_business, get_system_prompt_for_business


client = OpenAI()

with open("./data/toy_user_data.json", 'r') as file:
    data = json.load(file)


def recommend_person(project_description: Union[str, dict]) -> ListPeople:
    user_prompt = get_user_prompt_for_business(project_description)

    output = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": get_system_prompt_for_business(data)},
            {"role": "user","content": user_prompt}],
            response_format=ListPeople
        )
    
    return output.choices[0].message.parsed.people
