# Generated by Django 2.0.6 on 2018-06-11 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_task_exception_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_link', models.FileField(upload_to='')),
                ('uploaded_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
