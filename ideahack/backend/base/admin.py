from django.contrib import admin
from ideahack.backend.base.models import (
    Engineer,
    Researcher,
    Project,
    ResearchCenterRepresentative,
    CompanyRepresentative,
)

admin.site.register(Engineer)

admin.site.register(Researcher)

admin.site.register(Project)

admin.site.register(ResearchCenterRepresentative)

admin.site.register(CompanyRepresentative)
