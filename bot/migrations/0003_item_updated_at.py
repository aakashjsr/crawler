# Generated by Django 2.0.6 on 2018-06-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20180607_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
