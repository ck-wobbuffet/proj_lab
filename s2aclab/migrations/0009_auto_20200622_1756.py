# Generated by Django 2.0 on 2020-06-22 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s2aclab', '0008_auto_20200620_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='created_time',
            field=models.DateTimeField(),
        ),
    ]
