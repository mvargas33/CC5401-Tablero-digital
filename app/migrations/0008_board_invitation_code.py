# Generated by Django 2.2.6 on 2020-06-22 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20191222_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='invitation_code',
            field=models.TextField(default=''),
        ),
    ]