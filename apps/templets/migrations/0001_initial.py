# Generated by Django 2.0.6 on 2019-12-18 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Templet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='模板名称')),
                ('subject', models.CharField(max_length=40, verbose_name='邮件标题')),
                ('text', models.TextField(verbose_name='邮件内容')),
                ('attachments', models.FileField(upload_to='attach/%Y/%M')),
            ],
            options={
                'verbose_name': '邮件模板',
                'verbose_name_plural': '邮件模板',
            },
        ),
    ]
