from ideahack.backend.base.models import (
    Engineer,
    Researcher,
    ResearchCenterRepresentative,
    CompanyRepresentative,
)


def map_user_type(type_id: int):
    match type_id:
        case 0:
            return Researcher
        case 1:
            return Engineer
        case 2:
            return ResearchCenterRepresentative
        case 3:
            return CompanyRepresentative
        case _:
            raise ValueError(f"Invalid type_id: {type_id}")
