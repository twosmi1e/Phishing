# Generated by Django 2.0.6 on 2020-01-14 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0002_auto_20191218_1040'),
        ('pages', '0002_auto_20191226_1557'),
        ('smtp', '0002_auto_20191230_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='任务名称')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('launch_date', models.DateField(blank=True, verbose_name='开始时间')),
                ('sendby_date', models.DateField(blank=True, verbose_name='结束时间')),
                ('complete_date', models.DateField(verbose_name='完成时间')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contacts.Group', verbose_name='分组')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='smtp.EmailHeader', verbose_name='邮件头')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pages.Page', verbose_name='钓鱼页面')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='smtp.EmailServer', verbose_name='邮件服务器')),
            ],
            options={
                'verbose_name': '发送任务',
                'verbose_name_plural': '发送任务',
            },
        ),
    ]
