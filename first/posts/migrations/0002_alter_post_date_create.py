# Generated by Django 4.2.1 on 2023-06-09 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_create',
            field=models.DateTimeField(blank=True),
        ),
    ]
