import fire
from dotenv import load_dotenv

from ideahack.recommendations.recommend_person import recommend_person

load_dotenv()

def main(description: str):
    output = recommend_person(description)
    print(output)


if __name__ == "__main__":
    fire.Fire(main)
