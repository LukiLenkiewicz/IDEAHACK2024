

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('vector_id', models.IntegerField(null=True)),
                ('bio', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('location', models.TextField(blank=True)),
                ('keywords', models.TextField(blank=True)),
                ('services', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('bio', models.TextField(blank=True)),
                ('portfolio', models.TextField(blank=True)),
                ('interests', models.TextField(blank=True)),
                ('preferences', models.TextField(blank=True)),
                ('keywords', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('surname', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('vector_id', models.IntegerField(null=True)),
                ('bio', models.TextField(blank=True)),
                ('experience', models.TextField(blank=True)),
                ('skills', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('keywords', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('bio', models.TextField(blank=True)),
                ('owner_type', models.TextField(blank=True)),
                ('owner_id', models.PositiveIntegerField()),
                ('requirements', models.TextField(blank=True)),
                ('email', models.EmailField(max_length=200)),
                ('pitch_deck', models.TextField(blank=True)),
                ('area_of_research', models.TextField(blank=True)),
                ('cost_structure', models.PositiveBigIntegerField(blank=True)),
                ('keywords', models.TextField(blank=True)),
                ('vector_id', models.IntegerField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('available', models.BooleanField()),
                ('link', models.URLField(blank=True)),
                ('person_name', models.CharField(blank=True, max_length=255, null=True)),
                ('person_surname', models.CharField(blank=True, max_length=255, null=True)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='base.project')),
            ],
        ),
    ]
