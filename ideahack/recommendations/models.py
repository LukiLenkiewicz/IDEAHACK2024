from pydantic import BaseModel


class Person(BaseModel):
    name: str
    description: str


class ListPeople(BaseModel):
    people: list[Person]


class Project(BaseModel):
    name: str
    description: str


class ListProjects(BaseModel):
    projects: list[Project]
