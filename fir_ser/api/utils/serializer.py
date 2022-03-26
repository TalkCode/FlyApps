import logging
import os

from rest_framework import serializers

from api import models
from api.utils.apputils import bytes2human
from api.utils.modelutils import get_user_domain_name, get_app_domain_name, get_app_download_uri
from common.base.baseutils import get_choices_dict
from common.cache.storage import AdPicShowCache
from common.utils.caches import get_user_free_download_times, get_user_cert_auth_status
from common.utils.storage import Storage
from common.utils.token import make_token

logger = logging.getLogger(__name__)


def get_download_url_from_context(self, obj, key, url, force_new=False):
    download_url = ""
    if self.context.get("key", None) and self.context.get("key") != "undefined":
        key = self.context.get("key", '')
    if self.context.get("storage", None) and self.context.get("storage") != "undefined":
        storage = self.context.get("storage", None)
    else:
        if isinstance(obj, models.Apps):
            storage = Storage(obj.user_id)
        elif isinstance(obj, models.AppReleaseInfo):
            storage = Storage(obj.app_id.user_id)
        elif isinstance(obj, models.UserAdDisplayInfo):
            storage = Storage(obj.user_id)
        elif isinstance(obj, models.UserInfo):
            storage = Storage(obj)
        elif isinstance(obj, models.UserCertificationInfo) or isinstance(obj, models.CertificationInfo):
            storage = Storage(obj.user_id, None, True)
        else:
            storage = None
    if storage:
        download_url = storage.get_download_url(os.path.basename(url), 600, key, force_new)
        logger.info(f'get {os.path.basename(url)} download_url {download_url} force_new:{force_new} key:{key}')
    return download_url


def get_app_master_obj_from_context(self, obj):
    master_release_obj = models.AppReleaseInfo.objects.filter(app_id=obj, is_master=True).first()
    if self.context.get("release_id", None) and self.context.get("release_id") != "undefined":
        master_release_obj = models.AppReleaseInfo.objects.filter(app_id=obj,
                                                                  release_id=self.context.get("release_id")).first()
    return master_release_obj


def get_screenshots_from_self(self, obj, force_new=False):
    screenshots_list = []
    for screenshot_obj in models.AppScreenShot.objects.filter(app_id=obj).all():
        icon_url = get_download_url_from_context(self, obj, '', screenshot_obj.screenshot_url, force_new)
        screenshots_list.append({'id': screenshot_obj.pk, 'url': icon_url})
    return screenshots_list


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["username", "uid", "mobile", "job", "email", "domain_name", "role", "first_name",
                  'head_img', 'storage_active', 'supersign_active', 'free_download_times', 'download_times',
                  'certification', 'qrcode_domain_name']

    head_img = serializers.SerializerMethodField()

    def get_head_img(self, obj):
        return get_download_url_from_context(self, obj, '', obj.head_img)

    free_download_times = serializers.SerializerMethodField()

    def get_free_download_times(self, obj):
        return get_user_free_download_times(obj.id, auth_status=get_user_cert_auth_status(obj.id))

    certification = serializers.SerializerMethodField()

    def get_certification(self, obj):
        auth_status = -1
        certification_obj = models.UserCertificationInfo.objects.filter(user_id=obj).first()
        if certification_obj:
            auth_status = certification_obj.status
        return auth_status

    domain_name = serializers.SerializerMethodField()

    def get_domain_name(self, obj):
        return get_user_domain_name(obj)

    qrcode_domain_name = serializers.SerializerMethodField()

    def get_qrcode_domain_name(self, obj):
        if obj.role and obj.role > 1:
            return get_user_domain_name(obj, 0)


class AppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apps
        exclude = ["user_id", "id"]

    has_combo = serializers.SerializerMethodField()

    def get_has_combo(self, obj):
        if obj.has_combo:
            obj.has_combo.has_combo = None
            return AppsListSerializer(obj.has_combo, context=self.context).data

    preview_url = serializers.SerializerMethodField()

    def get_preview_url(self, obj):
        return get_app_download_uri(None, obj.user_id, obj)

    private_developer_number = serializers.IntegerField(default=0)
    count = serializers.IntegerField(default=0)
    #
    # def get_private_developer_number(self, obj):
    #     return models.AppleDeveloperToAppUse.objects.filter(app_id=obj).count()
    #
    private_developer_used_number = serializers.IntegerField(default=0)
    #
    # def get_private_developer_used_number(self, obj):
    #     return models.DeveloperDevicesID.objects.filter(app_id=obj,
    #                                                     developerid__appledevelopertoappuse__app_id=obj).distinct().count()

    domain_name = serializers.SerializerMethodField()

    def get_domain_name(self, obj):
        return get_app_domain_name(obj)

    sign_type_choice = serializers.SerializerMethodField()

    def get_sign_type_choice(self, obj):
        return get_choices_dict(obj.supersign_type_choices)

    supersign_used_number = serializers.IntegerField(default=0)
    #
    # def get_supersign_used_number(self, obj):
    #     return models.APPSuperSignUsedInfo.objects.filter(app_id=obj).all().count()
    #
    developer_used_count = serializers.IntegerField(default=0)
    #
    # def get_developer_used_count(self, obj):
    #     return models.DeveloperAppID.objects.filter(app_id=obj).all().count()

    screenshots = serializers.SerializerMethodField()

    def get_screenshots(self, obj):
        return get_screenshots_from_self(self, obj)

    master_release = serializers.SerializerMethodField()

    def get_master_release(self, obj):
        master_release_obj = get_app_master_obj_from_context(self, obj)
        if master_release_obj:
            key = ''
            icon_url = get_download_url_from_context(self, obj, key, master_release_obj.icon_url)
            datainfo = {
                "app_version": master_release_obj.app_version,
                "icon_url": icon_url,
                "build_version": master_release_obj.build_version,
                "release_type": master_release_obj.release_type,
                "minimum_os_version": master_release_obj.minimum_os_version,
                "created_time": master_release_obj.created_time,
                "binary_size": bytes2human(master_release_obj.binary_size),
                "release_id": master_release_obj.release_id,
                "changelog": master_release_obj.changelog,
                "binary_url": master_release_obj.binary_url,
            }

            download_token = make_token(master_release_obj.release_id, 600, key=key)
            datainfo["download_token"] = download_token
            udid_lists = []
            try:
                udid_data = eval(master_release_obj.udid)
                for udid in udid_data:
                    udid_lists.append({'udid': udid})
            except Exception as e:
                pass
            datainfo["udid"] = udid_lists

            return datainfo
        else:
            return {}


class AppsListSerializer(AppsSerializer):
    class Meta:
        model = models.Apps
        fields = ["app_id", "bundle_id", "issupersign", "name", "preview_url", "short", "type", "master_release",
                  "has_combo"]

    def get_master_release(self, obj):
        master_release_obj = get_app_master_obj_from_context(self, obj)
        if master_release_obj:
            key = ''
            icon_url = get_download_url_from_context(self, obj, key, master_release_obj.icon_url)
            datainfo = {
                "app_version": master_release_obj.app_version,
                "icon_url": icon_url,
                "build_version": master_release_obj.build_version,
                "binary_size": bytes2human(master_release_obj.binary_size),
                "binary_url": master_release_obj.binary_url,
                "release_type": master_release_obj.release_type,
            }
            return datainfo
        else:
            return {}

    def get_has_combo(self, obj):
        if obj.has_combo:
            obj.has_combo.has_combo = None
            return AppsListSerializer(obj.has_combo, context=self.context).data


class AppsQrListSerializer(AppsListSerializer):
    class Meta:
        model = models.Apps
        fields = ["app_id", "bundle_id", "name", "preview_url", "short", "type", "master_release"]

    def get_master_release(self, obj):
        master_release_obj = get_app_master_obj_from_context(self, obj)
        if master_release_obj:
            key = ''
            icon_url = get_download_url_from_context(self, obj, key, master_release_obj.icon_url)
            datainfo = {
                "app_version": master_release_obj.app_version,
                "icon_url": icon_url,
                "build_version": master_release_obj.build_version,
                "binary_url": master_release_obj.binary_url,
                "release_type": master_release_obj.release_type,
            }
            return datainfo
        else:
            return {}


class AppsShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apps
        fields = ["app_id", "name", "short", "has_combo", "isshow", "description", "need_password", 'master_release',
                  'type', 'issupersign', 'wxeasytype', 'wxredirect', 'domain_name', 'screenshots']

    screenshots = serializers.SerializerMethodField()

    def get_screenshots(self, obj):
        return get_screenshots_from_self(self, obj, True)

    domain_name = serializers.SerializerMethodField()

    def get_domain_name(self, obj):
        return get_app_domain_name(obj)

    need_password = serializers.SerializerMethodField()

    def get_need_password(self, obj):
        if obj.password != '':
            return True
        return False

    has_combo = serializers.SerializerMethodField()

    def get_has_combo(self, obj):
        if obj.has_combo:
            obj.has_combo.has_combo = None
            if obj.has_combo.isshow and obj.has_combo.status == 1:
                return AppsShortSerializer(obj.has_combo, context=self.context).data

    master_release = serializers.SerializerMethodField()

    def get_master_release(self, obj):
        master_release_obj = get_app_master_obj_from_context(self, obj)
        if master_release_obj:
            key = ''
            if self.context.get("key", None) and self.context.get("key") != "undefined":
                key = self.context.get("key", '')
            icon_url = get_download_url_from_context(self, obj, key, os.path.basename(master_release_obj.icon_url),
                                                     True)
            datainfo = {
                "app_version": master_release_obj.app_version,
                "icon_url": icon_url,
                "build_version": master_release_obj.build_version,
                "release_type": master_release_obj.release_type,
                "created_time": master_release_obj.created_time,
                "binary_size": bytes2human(master_release_obj.binary_size),
                "release_id": master_release_obj.release_id,
                "changelog": master_release_obj.changelog,
                "binary_url": master_release_obj.binary_url,
            }

            download_token = make_token(master_release_obj.release_id, 600, key=key, force_new=True)
            datainfo["download_token"] = download_token
            return datainfo
        else:
            return {}


class AppReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppReleaseInfo
        fields = ["app_version", "icon_url", "build_version",
                  "release_type", "minimum_os_version",
                  "created_time", "binary_size", "release_id", "size", "type", "editing", "master_color", "changelog",
                  "is_master", 'download_token', 'binary_url', 'udid', 'distribution_name']

    download_token = serializers.SerializerMethodField()
    size = serializers.CharField(default='large')
    type = serializers.CharField(default='primary')
    editing = serializers.SerializerMethodField()
    master_color = serializers.SerializerMethodField()
    icon_url = serializers.SerializerMethodField()
    binary_size = serializers.SerializerMethodField()
    udid = serializers.SerializerMethodField()

    def get_udid(self, obj):
        udid_lists = []
        try:
            udid_data = eval(obj.udid)
            for udid in udid_data:
                udid_lists.append({'udid': udid})
        except Exception as e:
            pass
        return udid_lists

    def get_binary_size(self, obj):
        return bytes2human(obj.binary_size)

    def get_download_token(self, obj):
        return make_token(obj.release_id, 600)

    def get_icon_url(self, obj):
        return get_download_url_from_context(self, obj, '', os.path.basename(obj.icon_url))

    def get_master_color(self, obj):
        if obj.is_master:
            return '#0bbd87'

    def get_editing(self, obj):
        return {"changelog": False, "binary_url": False}


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppStorage
        exclude = ["user_id"]

    storage_type_display = serializers.CharField(source="get_storage_type_display", read_only=True)

    download_auth_type_choices = serializers.SerializerMethodField()

    # secret_key = serializers.SerializerMethodField()
    # 加上此选项，会导致update获取不到值
    # def get_secret_key(self, obj):
    #     return ''

    # def validate_secret_key(self, secret_key):
    #     ...

    def get_download_auth_type_choices(self, obj):
        return get_choices_dict(obj.download_auth_type_choices)

    def create(self, validated_data):
        if self.context.get("user_obj", None) and self.context.get("user_obj") != "undefined":
            user_obj = self.context.get("user_obj", None)
            if user_obj:
                storage_obj = models.AppStorage.objects.create(**validated_data, user_id=user_obj)
                return storage_obj
        return None

    def update(self, instance, validated_data):
        secret_key = validated_data.get('secret_key', '')
        if secret_key != "" and secret_key != instance.secret_key:
            ...
        else:
            validated_data['secret_key'] = instance.secret_key
        return super().update(instance, validated_data)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        exclude = ["id"]


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        exclude = ["id"]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CertificationInfo
        fields = ["certification_url", "type"]

    certification_url = serializers.SerializerMethodField()

    def get_certification_url(self, obj):
        return get_download_url_from_context(self, obj, '', obj.certification_url)


class UserCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserCertificationInfo
        exclude = ["id", "user_id", "created_time"]


class ThirdWxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ThirdWeChatUserInfo
        exclude = ["id", "sex", "address", "user_id"]


class DomainNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDomainInfo
        exclude = ["id", "user_id"]

    app_info = serializers.SerializerMethodField()

    def get_app_info(self, obj):
        app_obj = obj.app_id
        if app_obj:
            app_info = {
                'app_id': app_obj.app_id,
                'name': app_obj.name,
            }
            return app_info
        return {}


class UserAdInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAdDisplayInfo
        exclude = ["user_id"]

    ad_pic = serializers.SerializerMethodField()

    def get_ad_pic(self, obj):
        return get_download_url_from_context(self, obj, '', obj.ad_pic)


class AppAdInfoSerializer(UserAdInfoSerializer):
    class Meta:
        model = models.UserAdDisplayInfo
        fields = ["ad_uri", "ad_pic"]

    ad_pic = serializers.SerializerMethodField()

    def get_ad_pic(self, obj):
        AdPicShowCache(self.context.get("key", ''), self.context.get("short", '')).set_storage_cache(obj.ad_pic)
        return get_download_url_from_context(self, obj, '', obj.ad_pic, True)


class AppReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppReportInfo
        exclude = ["id"]


class NotifyReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotifyReceiver
        exclude = ["user_id"]

    weixin = serializers.SerializerMethodField()

    def get_weixin(self, obj):
        return ThirdWxSerializer(obj.weixin).data


class NotifyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotifyConfig
        exclude = ["user_id", "sender"]

    senders = serializers.SerializerMethodField()

    def get_senders(self, obj):
        return NotifyReceiverSerializer(obj.sender, many=True).data
