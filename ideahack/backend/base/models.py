from email.policy import default
from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.TextField()
    id = models.IntegerField(primary_key=True)

    description = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    website = models.URLField(max_length=200, blank=True)
    social_media = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name}  {self.surname}"

    def get_urls(self):
        return [url.strip() for url in self.other_urls.split(",")]


class Project(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    id = models.IntegerField(primary_key=True)

    description = models.TextField(blank=True)
    field = models.TextField(blank=True)
    funds = models.IntegerField()
    available_positions = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.TextField()

    id = models.IntegerField(primary_key=True)

    description = models.TextField(blank=True)

    projects = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Investor(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.TextField()

    id = models.IntegerField(primary_key=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
