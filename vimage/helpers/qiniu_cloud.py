# -*- coding: utf-8 -*-
import os
import random
from io import BytesIO
import requests as req
from PIL import Image, ImageDraw, ImageFont
from qiniu import Auth, put_file, put_data
from .utils import timestamp, timestamp2string, MixGenId

__all__ = [
    'QiniuCloud',
    'QiniuError'
]


class QiniuError(Exception):
    def __init__(self, msg):
        super(QiniuError, self).__init__(msg)


class QiniuCloud(object):
    """七牛文件存储工具类"""

    def __init__(self, access_key, access_secret, bucket_name, domain_url=''):
        """初始化配置"""
        self.access_key = access_key
        self.access_secret = access_secret
        self.bucket_name = bucket_name
        self.domain_url = domain_url

    def get_token(self, path_key):
        # 七牛的配置
        q = Auth(self.access_key, self.access_secret)
        token = q.upload_token(self.bucket_name, path_key, 3600)

        return token

    def upload_content(self, content, path_key=None, folder_name=None):
        """
        上传内容到七牛

        :param content: 文件内容
        :param path_key: 图片key
        :param folder_name: 文件夹名称
        :return:
        """
        if path_key is None:
            path_key = QiniuCloud.gen_path_key()

        if folder_name:
            path_key = '%s/%s' % (folder_name, path_key)

        token = self.get_token(path_key)

        ret, info = put_data(token, path_key, content)

        print(ret)

        print(info)

        if ret['key'] != path_key:
            raise QiniuError('上传文件有误！')

        return path_key

    def upload_file(self, src, path_key=None, folder_name=None):
        """
        上传图片到七牛

        :param src: 图片路径
        :param path_key: 图片key
        :param folder_name: 文件夹名称
        :return: 上传成功后的图片url
        """
        if path_key is None:
            path_key = QiniuCloud.gen_path_key()

        if folder_name:
            path_key = '%s/%s' % (folder_name, path_key)

        token = self.get_token(path_key)

        # 上传图片
        if not os.path.exists(src):
            raise QiniuError('上传文件不存在！')

        ret, info = put_file(token, path_key, src)

        if ret['key'] == path_key:
            # 上传成功后删除静态图片
            QiniuCloud.remove_file(src)

        return path_key

    @staticmethod
    def up_token(access_key, access_secret, bucket_name, domain_url):
        """上传验证token"""
        q = Auth(access_key, access_secret)
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        save_key = '$(year)$(mon)$(day)/$(etag)$(ext)'
        policy = {
            'scope': bucket_name,
            'deadline': int(timestamp()) + 3600,
            'callbackUrl': '%s/open/qiniu/notify' % domain_url,
            'callbackBody': 'filepath=$(key)&filename=$(fname)&filesize=$(fsize)&mime=$(mimeType)&user_id=$(x:user_id)'
                            '&width=$(imageInfo.width)&height=$(imageInfo.height)&ext=$(ext)&directory=$(x:directory)',
            'saveKey': save_key,
            'fsizeLimit': 20 * 1024 * 1024,  # 限定上传文件大小最大值, 20M
            'returnUrl': '',
            'returnBody': ''
        }

        # 3600为token过期时间，秒为单位。3600等于一小时
        return q.upload_token(bucket_name, None, 3600, policy)

    @staticmethod
    def load_image(image_url):
        """
        加载图片 url

        :return: 图片实例
        """

        # 请求图片链接，生成图片
        r = req.get(image_url)
        image = Image.open(BytesIO(r.content)).convert('RGBA')

        return image

    @staticmethod
    def save_file(image, file_path):
        """
        保存图片

        :param image: 图片
        :param file_path: 文件夹路径
        """
        # 判断文件夹是否存在
        if os.path.exists(file_path):
            src_file = '%s/%s' % (file_path, QiniuCloud.gen_path_key())
            image.save(fp=src_file, format='PNG')

        return src_file

    @staticmethod
    def remove_file(src):
        """
        删除图片

        :param src: 图片路径
        """

        if os.path.exists(src):
            os.remove(src)

    @staticmethod
    def gen_path_key():
        """
        设置图片的path
        """

        # 根据时间戳生成文件名
        filename = '%s/%s%s' % (timestamp2string(timestamp(), '%Y%m%d'), MixGenId.gen_letters(20), '.png')

        return filename

    @staticmethod
    def gen_filename():
        """生成文件名"""
        return '%s.png' % MixGenId.gen_letters(20)
