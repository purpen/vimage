# -*- coding: utf-8 -*-
from flask import request, url_for, abort, g

from . import api
from vimage.models import Sensitive
from vimage.helpers.utils import *
from vimage.helpers.ocr import *


@api.route('/tools/hello_ocr', methods=['GET'])
def hello_ocr():
    """测试 ocr 功能"""

    return ocr_local_image()


@api.route('/tools/pick_sensitive', methods=['POST'])
def pick_sensitive():
    """智能识别敏感词"""
    image_url = request.json.get('images')

    # 测试
    # 读取图片，进行识别文本
    return ocr_url_image(image_url)
