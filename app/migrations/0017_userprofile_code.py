# Generated by Django 5.0.6 on 2024-09-23 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_userprofile_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='code',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]