from email.policy import default
from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models


class _User(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to="profile-images", default="blank-profile-picture.png"
    )
    location = models.CharField(max_length=100, blank=True)
    work_expirience = models.TextField(blank=True)
    research_papers = models.TextField(blank=True)
    projects = models.TextField(blank=True)

    linkedin = models.URLField(max_length=200)
    github = models.URLField(max_length=200)
    google_scholar = models.URLField(max_length=200)
    other_urls = models.TextField(help_text="Enter other URLs separated by commas")

    def __str__(self):
        return f"{self.name}  {self.surname}"

    def get_urls(self):
        return [url.strip() for url in self.other_urls.split(",")]


class Engineer(_User):
    pass


class Researcher(_User):
    pass


class Project(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    id_project = models.IntegerField()
    bio = models.TextField(blank=True)
    field = models.TextField(blank=True)
    funds = models.IntegerField()
    available_positions = models.TextField(blank=True)
    occupied_positions = models.TextField(blank=True)

    def __str__(self):
        return self.name


class _Representative(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    id_representative = models.IntegerField()
    bio = models.TextField(blank=True)
    img = models.ImageField(
        upload_to="profile-images", default="blank-profile-picture.png"
    )
    location = models.CharField(max_length=100, blank=True)
    history = models.TextField(blank=True)

    projects = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="projects"
    )

    def __str__(self):
        return self.name


class CompanyRepresentative(_Representative):
    pass


class ResearchCenterRepresentative(_Representative):
    pass
