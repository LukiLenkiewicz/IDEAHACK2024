from typing import Union


def get_user_prompt_for_business(description: Union[str, dict]) -> str:
    user_prompt = f"""
    Give a list of people that fit best for given description: {description}. 
    As long as possible use non technical language. User is a business person 
    not an engineer.
    """
    
    return user_prompt


def get_system_prompt_for_business(data: dict) -> str:
    summary_prompt = f"""
    People: {data}

    Instructions: I gave you list of experts with different specializations and expertise in different fields. 
    You need to provide information about experts which skills that fit best for description provided by the user.
    """
    return summary_prompt


def get_user_prompt_for_regular_user(description: Union[str, dict]) -> str:
    user_prompt = f"Give a list of projects that fit best for given description: {description}. "
    return user_prompt


def get_system_prompt_for_regular_user(data: dict) -> str:
    summary_prompt = f"""
    Projects: {data}

    Instructions: I gave you list of different projects. You need to recommend best projects for given user based
    on their description.
    """
    return summary_prompt