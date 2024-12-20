from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import uuid


class User(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.TextField()
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)

    vector_id = models.IntegerField(null=True)

    bio = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    link = models.URLField(max_length=200, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}  {self.surname}"

    def get_urls(self):
        return [url.strip() for url in self.other_urls.split(",")]


class Project(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)

    bio = models.TextField(blank=True)

    owner_type = models.TextField(blank=True)
    owner_id = models.CharField(max_length=36)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    owner = GenericForeignKey("content_type", "owner_id")

    requirements = models.TextField(blank=True)
    email = models.EmailField(max_length=200)
    pitch_deck = models.URLField(max_length=300, blank=True)
    area_of_research = models.TextField(blank=True)
    cost_structure = models.PositiveBigIntegerField(blank=True)
    keywords = models.TextField(blank=True)
    vector_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, null=True, blank=True)
    available = models.BooleanField()

    link = models.URLField(max_length=200, blank=True)
    person_name = models.CharField(max_length=255, null=True, blank=True)
    person_surname = models.CharField(max_length=255, null=True, blank=True)

    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="projects",
    )


class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.TextField()

    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)

    vector_id = models.IntegerField(null=True)

    bio = models.TextField(blank=True)

    link = models.URLField(max_length=200, blank=True)
    location = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    services = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Investor(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.TextField()

    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)

    bio = models.TextField(blank=True)

    portfolio = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    preferences = models.TextField(blank=True)
    keywords = models.TextField(blank=True)

    def __str__(self):
        return self.name
