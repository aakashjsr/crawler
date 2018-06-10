# Generated by Django 2.0.6 on 2018-06-10 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_item_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=25)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('item_codes', models.CharField(max_length=5000)),
                ('check_in_stock', models.BooleanField(default=False)),
            ],
        ),
    ]
