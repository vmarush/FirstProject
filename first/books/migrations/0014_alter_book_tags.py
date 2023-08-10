# Generated by Django 4.2.1 on 2023-06-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_alter_publisher_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='books', to='books.tag'),
        ),
    ]
