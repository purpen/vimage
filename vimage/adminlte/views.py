# -*- coding: utf-8 -*-
from flask import render_template

from . import adminlte


@adminlte.route('/')
def dashboard():
    """管理控制台"""
    features = [
        '智能海报生成', '智能Banner生成', '社交图文生成', '图片添加二维码', '广告违禁词识别', '一键生成主图短视频', '智能图像压缩', '以图搜图比价',
        '图像识别商品标注', '图片情感分析', '智能生成PPT', 'GIF动图制作'
    ]
    return render_template('adminlte/dashboard.html',
                           features=features)
