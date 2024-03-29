# Generated by Django 4.2.1 on 2023-06-12 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.category'),
        ),
    ]
