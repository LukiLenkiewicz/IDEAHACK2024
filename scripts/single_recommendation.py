import fire
from dotenv import load_dotenv

from ideahack.recommendations import recommend_person
from ideahack.recommendations import recommend_project

load_dotenv()

class Recommend:
    def business(self, description):
        output = recommend_person(description)
        print(output)

    def person(self, description):
        output = recommend_project(description)
        print(output)

    def ivnestor(self, description):
        output = recommend_project(description)
        print(output)


if __name__ == "__main__":
    fire.Fire(Recommend)
