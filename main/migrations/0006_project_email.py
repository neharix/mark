# Generated by Django 5.0 on 2024-10-02 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_directions_project_direction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='email',
            field=models.EmailField(default='a@g.com', max_length=254, verbose_name='Email'),
            preserve_default=False,
        ),
    ]
