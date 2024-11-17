from django.contrib import admin
from ideahack.backend.base.models import User, Project, Company, Investor


admin.site.register(User)

admin.site.register(Project)

admin.site.register(Company)

admin.site.register(Investor)
