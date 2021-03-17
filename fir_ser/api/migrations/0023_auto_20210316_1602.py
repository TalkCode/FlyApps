# Generated by Django 3.0.3 on 2021-03-16 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0022_appreleaseinfo_distribution_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppScreenShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot_url', models.CharField(blank=True, max_length=128, verbose_name='应用截图URL')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
            ],
            options={
                'verbose_name': '应用截图',
                'verbose_name_plural': '应用截图',
            },
        ),
        migrations.AddIndex(
            model_name='appscreenshot',
            index=models.Index(fields=['app_id'], name='api_appscre_app_id__b65655_idx'),
        ),
    ]
