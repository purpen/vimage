# -*- coding: utf-8 -*-
from flask import request, url_for, abort, g

from . import api
from vimage.models import Sensitive
from vimage.helpers.utils import *


@api.route('/tools/pick_sensitive', methods=['POST'])
def pick_sensitive():
    """智能识别敏感词"""
    image_url = request.json.get('image')

    # 读取图片，进行识别文本
