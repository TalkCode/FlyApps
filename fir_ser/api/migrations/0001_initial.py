# Generated by Django 3.0.3 on 2020-05-01 16:40

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='用户名')),
                ('email',
                 models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('uid', models.CharField(db_index=True, max_length=64, unique=True)),
                ('mobile', models.BigIntegerField(help_text='用于手机验证码登录', null=True, unique=True, verbose_name='手机')),
                ('qq', models.BigIntegerField(blank=True, db_index=True, null=True, verbose_name='QQ')),
                ('is_active', models.BooleanField(default=True, verbose_name='账户状态，默认启用')),
                ('job', models.TextField(blank=True, max_length=128, null=True, verbose_name='职位')),
                ('company', models.CharField(blank=True, max_length=128, null=True, verbose_name='公司')),
                ('gender',
                 models.SmallIntegerField(choices=[(0, '保密'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('head_img', models.CharField(default='head_img.jpeg', max_length=256, verbose_name='个人头像')),
                ('role', models.SmallIntegerField(choices=[(0, '普通会员'), (1, 'VIP'), (2, 'SVIP'), (3, '管理员')], default=0,
                                                  verbose_name='角色')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('download_times', models.IntegerField(default=100, verbose_name='下载次数')),
                ('all_download_times', models.BigIntegerField(default=0, verbose_name='总共下载次数')),
                ('domain_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='域名')),
                ('history_release_limit',
                 models.IntegerField(blank=True, default=10, null=True, verbose_name='app 历史记录版本')),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group',
                                                  verbose_name='groups')),
            ],
            options={
                'verbose_name': '账户信息',
                'verbose_name_plural': '账户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AppIOSDeveloperInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='开发者标识')),
                ('email',
                 models.EmailField(blank=True, max_length=64, null=True, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=64)),
                ('is_actived', models.BooleanField(default=False, verbose_name='是否已经激活')),
                ('certid', models.CharField(blank=True, max_length=64, null=True, verbose_name='超级签名自动创建证书ID')),
                ('usable_number', models.IntegerField(default=100, verbose_name='可使用设备数')),
                ('use_number', models.IntegerField(default=0, verbose_name='已消耗设备数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '苹果开发者账户',
                'verbose_name_plural': '苹果开发者账户',
            },
        ),
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(db_index=True, max_length=64, unique=True)),
                ('type', models.SmallIntegerField(choices=[(0, 'android'), (1, 'ios')], default=0, verbose_name='类型')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='应用名称')),
                ('short', models.CharField(db_index=True, max_length=16, unique=True, verbose_name='短链接')),
                ('bundle_id', models.CharField(blank=True, max_length=64, verbose_name='bundle id')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('count_hits', models.BigIntegerField(default=0, verbose_name='下载次数')),
                ('password', models.CharField(default='', help_text='默认 没有密码', max_length=32, verbose_name='访问密码')),
                ('isshow', models.BigIntegerField(default=1, verbose_name='下载页可见')),
                ('issupersign', models.BigIntegerField(default=False, verbose_name='是否超级签名包')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='描述')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('has_combo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                   related_name='combo_app_info', to='api.Apps', verbose_name='关联应用')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '应用信息',
                'verbose_name_plural': '应用信息',
            },
        ),
        migrations.CreateModel(
            name='VerifyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=32, verbose_name='真实姓名')),
                ('id_card', models.CharField(blank=True, max_length=32, null=True, verbose_name='身份证号或护照号')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='联系地址')),
                ('mobile', models.BigIntegerField(blank=True, null=True, verbose_name='联系电话')),
                ('date_verify', models.DateTimeField(auto_now_add=True, verbose_name='认证时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verify_info',
                                              to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '实名认证',
                'verbose_name_plural': '实名认证',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=64, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token',
                                           to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
        ),
        migrations.CreateModel(
            name='AppUDID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('udid', models.CharField(db_index=True, max_length=64, verbose_name='udid唯一标识')),
                ('product', models.CharField(blank=True, max_length=64, null=True, verbose_name='产品')),
                ('serial', models.CharField(blank=True, max_length=64, null=True, verbose_name='序列号')),
                ('version', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('imei', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('iccid', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_signed', models.BooleanField(default=False, verbose_name='是否完成签名打包')),
                ('binary_file', models.CharField(blank=True, max_length=128, null=True, verbose_name='签名包名称')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
            ],
            options={
                'verbose_name': '设备详情',
                'verbose_name_plural': '设备详情',
                'unique_together': {('app_id', 'udid')},
            },
        ),
        migrations.CreateModel(
            name='APPSuperSignUsedInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
                ('developerid',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppIOSDeveloperInfo',
                                   verbose_name='所使用苹果开发者账户')),
                ('udid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppUDID',
                                           verbose_name='所消耗的udid')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '设备使用统计',
                'verbose_name_plural': '设备使用统计',
            },
        ),
        migrations.CreateModel(
            name='AppStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='存储名字')),
                ('storage_type',
                 models.SmallIntegerField(choices=[(0, '本地存储'), (1, '七牛云存储'), (2, '阿里云存储'), (3, '默认存储')], default=3,
                                          verbose_name='存储类型')),
                ('access_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='存储访问key')),
                ('secret_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='存储访问secret')),
                (
                    'bucket_name',
                    models.CharField(blank=True, max_length=128, null=True, verbose_name='存储空间bucket_name')),
                ('domain_name',
                 models.CharField(blank=True, help_text='fly-storage.dvcloud.xin,可以自定义端口', max_length=128, null=True,
                                  verbose_name='下载域名')),
                ('is_https', models.BooleanField(default=True, verbose_name='是否支持https')),
                ('additionalparameters',
                 models.TextField(blank=True, default=None, help_text='阿里云:{"sts_role_arn":"arn信息","endpoint":""} ',
                                  null=True, verbose_name='额外参数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '存储配置',
                'verbose_name_plural': '存储配置',
            },
        ),
        migrations.CreateModel(
            name='AppReleaseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_master', models.BooleanField(default=True, verbose_name='是否master版本')),
                (
                    'release_id',
                    models.CharField(db_index=True, max_length=64, unique=True, verbose_name='release 版本id')),
                ('build_version', models.CharField(blank=True, max_length=16, verbose_name='build版本')),
                ('app_version', models.CharField(blank=True, max_length=16, verbose_name='app版本')),
                ('release_type',
                 models.SmallIntegerField(choices=[(0, 'android'), (1, 'adhoc'), (2, 'Inhouse'), (3, 'unknown')],
                                          default=0, verbose_name='版本类型')),
                ('minimum_os_version', models.CharField(max_length=64, verbose_name='应用可安装的最低系统版本')),
                ('binary_size', models.BigIntegerField(verbose_name='应用大小')),
                ('binary_url', models.CharField(blank=True, max_length=128, verbose_name='第三方下载URL')),
                ('icon_url', models.CharField(blank=True, max_length=128, verbose_name='图标url')),
                ('changelog', models.TextField(blank=True, default=None, null=True, verbose_name='更新日志')),
                ('udid', models.TextField(blank=True, default='', null=True, verbose_name='ios内测版 udid')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
            ],
            options={
                'verbose_name': '应用详情',
                'verbose_name_plural': '应用详情',
            },
        ),
        migrations.AddField(
            model_name='userinfo',
            name='storage',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                       related_name='app_storage', to='api.AppStorage', verbose_name='存储'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                         related_name='user_set', related_query_name='user', to='auth.Permission',
                                         verbose_name='user permissions'),
        ),
        migrations.AddIndex(
            model_name='apps',
            index=models.Index(fields=['app_id'], name='api_apps_app_id_4c0254_idx'),
        ),
        migrations.AddIndex(
            model_name='apps',
            index=models.Index(fields=['id', 'user_id', 'type'], name='api_apps_id_226a6b_idx'),
        ),
    ]
