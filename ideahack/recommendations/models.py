from pydantic import BaseModel


class Person(BaseModel):
    name: str
    description: str

class ListPeople(BaseModel):
    people: list[Person]
