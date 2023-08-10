# Generated by Django 4.2.1 on 2023-05-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='autor',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.IntegerField(blank=True),
        ),
    ]
