# -*- coding:utf-8 -*-
from io import BytesIO
import requests as req
from PIL import Image
from vimage.helpers.utils import *
from vimage.constant import *


def load_url_image(image_url, is_create=False):
    """
    通过 url 加载图片

    :param image_url: 图片链接
    :param is_create: 链接获取失败时是否创建图片
    :return:
    """

    # 默认创建的图片
    image = Image.new('RGBA', Size.DEFAULT_IMAGE_SIZE['square'], Colors.DEFAULT_BACKGROUND_COLOR['white']).copy()

    # 图片链接是否存在
    if not image_url:
        return image if is_create else custom_response('图片链接不存在', 400, False)

    # 请求图片链接，生成图片
    try:
        r = req.get(image_url)
        image = Image.open(BytesIO(r.content)).copy().convert('RGBA')

    except (req.exceptions.HTTPError, req.exceptions.URLRequired):
        return image if is_create else custom_response('图片链接获取失败', 400, False)

    return image
