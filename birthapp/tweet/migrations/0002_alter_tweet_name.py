# Generated by Django 5.1.2 on 2024-10-27 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='name',
            field=models.CharField(max_length=16),
        ),
    ]
