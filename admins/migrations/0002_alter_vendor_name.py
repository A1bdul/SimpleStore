# Generated by Django 4.1.5 on 2023-03-09 20:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admins", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="name",
            field=models.CharField(max_length=500, unique=True),
        ),
    ]