from typing import Union
import json
from openai import OpenAI

from ideahack.recommendations.models import ListProjects
from ideahack.recommendations.prompts import get_user_prompt_for_regular_user, get_system_prompt_for_regular_user


client = OpenAI()

with open("./data/businesses_toy_data.json", 'r') as file:
    data = json.load(file)


def recommend_project(person_description: Union[str, dict]) -> ListProjects:
    user_prompt = get_user_prompt_for_regular_user(person_description)

    output = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": get_system_prompt_for_regular_user(data)},
            {"role": "user","content": user_prompt}],
            response_format=ListProjects
        )
    
    return output.choices[0].message.parsed.projects
