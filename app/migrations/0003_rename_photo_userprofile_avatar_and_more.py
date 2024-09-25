# Generated by Django 5.0.6 on 2024-09-20 12:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='photo',
            new_name='avatar',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cv',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='id_photo',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]