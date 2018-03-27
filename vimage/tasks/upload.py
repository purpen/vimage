# -*- coding: utf-8 -*-
from flask import current_app
from vimage.extensions import fsk_celery

from vimage import db
from vimage.models import ImageSet
from vimage.helpers import QiniuCloud, QiniuError

FAIL = 'FAIL'
SKIP = 'SKIP'
SUCCESS = 'SUCCESS'


@fsk_celery.task(name='upload.qiniu_file')
def upload_qiniu_content(content, path_key):
    """上传文件至七牛"""

    qiniu_cloud = QiniuCloud(fsk_celery.conf['QINIU_ACCESS_KEY'], fsk_celery.conf['QINIU_ACCESS_SECRET'],
                             fsk_celery.conf['QINIU_BUCKET_NAME'])
    
    try:
        qiniu_cloud.upload_content(content, path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload error: %s' % str(err))
        return FAIL

    return SUCCESS
