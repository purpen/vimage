# -*- coding: utf-8 -*-
import io
from flask import current_app
from vimage.extensions import fsk_celery

from vimage import db
from vimage.models import ImageSet
from vimage.helpers import QiniuCloud, QiniuError, Poster
from vimage.helpers.poster_style import GoodsWxaStyle, GoodsSalesStyle
from vimage.constant import *

FAIL = 'FAIL'
SKIP = 'SKIP'
SUCCESS = 'SUCCESS'


@fsk_celery.task(name='maker.wxacode_image')
def make_wxacode_image(path_key, data, style_id):
    """生成并上传小程序码图片至七牛"""

    # 1、获取样式数据
    poster_style = GoodsWxaStyle(data, style_id)
    # 2、生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make()

    # 3、获取图像二进制流
    poster_content = io.BytesIO()
    poster_image.save(poster_content, 'png', optimize=True, quality=ImageInfo.SAVE_IMAGE_QUALITY)

    # 4、上传图片至云服务
    qiniu_cloud = QiniuCloud(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_ACCESS_SECRET'],
                             current_app.config['QINIU_BUCKET_NAME'])
    try:
        qiniu_cloud.upload_content(poster_content.getvalue(), path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload wxacode error: %s' % str(err))
        return FAIL

    return SUCCESS


@fsk_celery.task(name='maker.promotion_image')
def make_promotion_image(path_key, data, style_id):
    """生成并上传促销海报至七牛"""

    # 1、获取样式数据
    poster_style = GoodsSalesStyle(data, style_id)
    # 2、生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make()

    # 3、获取图像二进制流
    poster_content = io.BytesIO()
    poster_image.save(poster_content, 'png', optimize=True, quality=ImageInfo.SAVE_IMAGE_QUALITY)

    # 4、上传图片至云服务
    qiniu_cloud = QiniuCloud(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_ACCESS_SECRET'],
                             current_app.config['QINIU_BUCKET_NAME'])
    try:
        qiniu_cloud.upload_content(poster_content.getvalue(), path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload promotion error: %s' % str(err))
        return FAIL

    return SUCCESS
