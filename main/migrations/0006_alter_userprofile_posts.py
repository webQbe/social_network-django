# Generated by Django 5.1 on 2024-09-06 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_userprofile_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='posts',
            field=models.TextField(default='0'),
        ),
    ]
