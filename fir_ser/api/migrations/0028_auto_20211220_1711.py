# Generated by Django 3.2.3 on 2021-12-20 17:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0027_appiosdeveloperinfo_app_limit_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdomaininfo',
            name='is_https',
            field=models.BooleanField(default=False, verbose_name='是否支持HTTPS'),
        ),
        migrations.AddField(
            model_name='userdomaininfo',
            name='weight',
            field=models.IntegerField(default=10, verbose_name='下载页域名展示权重'),
        ),
    ]
