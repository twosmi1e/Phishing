# Generated by Django 2.0.6 on 2020-03-10 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smtp', '0002_auto_20191230_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailserver',
            name='mail_pass',
            field=models.CharField(max_length=50, verbose_name='授权口令'),
        ),
        migrations.AlterField(
            model_name='emailserver',
            name='mail_user',
            field=models.CharField(max_length=50, verbose_name='用户名'),
        ),
    ]
