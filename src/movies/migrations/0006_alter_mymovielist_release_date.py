# Generated by Django 5.1.4 on 2025-01-19 15:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0005_alter_mymovielist_vote_average"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mymovielist",
            name="release_date",
            field=models.DateField(null=True),
        ),
    ]
