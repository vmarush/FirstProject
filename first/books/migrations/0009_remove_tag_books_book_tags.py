# Generated by Django 4.2.1 on 2023-05-30 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='books',
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(related_name='books', to='books.tag'),
        ),
    ]
