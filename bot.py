import ast

from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI


class Form(BaseModel):
    name: str
    surname: str
    description: str

load_dotenv()

client = OpenAI()

form = {
   "name": None,
   "surname": None,
   "description": None,
   "experience": None,
   "email": None
}

system_prompt = f"""
You are a chatbot that helps users with creating their account. Use user's first 
message to fill as much information as possible. After first answers 
continue asking about not filled fields. Account is created when there are 
no None values in form: {form}. At the end display whole form so user can verify 
whether provided information is true or not. When form is filled say that they 
can type 'quit' to exit.
"""

def chatbot():
    messages = [
    {"role": "system", "content": system_prompt},
    ]

    print("Tell me about yourself: ")

    while True:
        message = input("User: ")

        if message.lower() == "quit":
            break

        messages.append({"role": "user", "content": message})

        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages
            )

        chat_message = response.choices[0].message.content
        print(chat_message)
        messages.append({"role": "assistant", "content": chat_message})
    
    messages.append({"role": "user", "content": "Display full filled form in .json format."})
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        response_format=Form
        )
    filled_form = response.choices[0].message.content
    
    return ast.literal_eval(filled_form)

if __name__ == "__main__":
    chatbot()