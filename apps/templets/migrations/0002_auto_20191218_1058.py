# Generated by Django 2.0.6 on 2019-12-18 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templet',
            name='attachments',
            field=models.FileField(blank=True, upload_to='attach/%Y/%M'),
        ),
    ]
