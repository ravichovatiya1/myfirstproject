# Generated by Django 3.1.5 on 2021-03-08 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20210308_2045'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
