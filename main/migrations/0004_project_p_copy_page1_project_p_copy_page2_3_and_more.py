# Generated by Django 5.1.1 on 2024-10-01 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_project_rated'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='p_copy_page1',
            field=models.ImageField(default='/', upload_to='passport_copies/1/', verbose_name='Topar ýolbaşçysynyň pasport nusgasy (sahypa 1)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='p_copy_page2_3',
            field=models.ImageField(default='/', upload_to='passport_copies/2-3/', verbose_name='Topar ýolbaşçysynyň pasport nusgasy (sahypa 2-3)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='p_copy_page32',
            field=models.ImageField(default='/', upload_to='passport_copies/32/', verbose_name='Topar ýolbaşçysynyň pasport nusgasy (sahypa 32)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='p_copy_page5_6',
            field=models.ImageField(default='/', upload_to='passport_copies/5-6/', verbose_name='Topar ýolbaşçysynyň pasport nusgasy (sahypa 5-6)'),
            preserve_default=False,
        ),
    ]
