# Generated by Django 2.0.6 on 2018-06-27 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_pet_arquivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='arquivo',
        ),
    ]
