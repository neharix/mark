# Generated by Django 5.1.1 on 2024-10-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_direction_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='rated',
            field=models.BooleanField(default=False),
        ),
    ]
