# -*- coding: utf-8 -*-
from qiniu import Auth
from .utils import timestamp

__all__ = [
    'QiniuStorage'
]


class QiniuStorage(object):
    """七牛文件存储工具类"""

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
