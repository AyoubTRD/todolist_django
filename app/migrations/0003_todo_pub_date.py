# Generated by Django 3.0.4 on 2020-03-20 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200320_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
