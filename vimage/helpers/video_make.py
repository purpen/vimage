# -*- coding:utf-8 -*-
import io
import requests as req
from flask import current_app
from vimage.constant import Fonts
from vimage.helpers.utils import *
from PIL import Image
import numpy as np
import imageio
imageio.plugins.ffmpeg.download()

from moviepy.editor import *


def _url_to_image(url):
    """
    通过 url 加载图片

    :param url: 图片链接
    :return: 图片
    """

    try:
        r = req.get(url)
        image = Image.open(io.BytesIO(r.content)).convert('RGB')

    except (req.exceptions.HTTPError, req.exceptions.URLRequired):
        return custom_response('图片链接获取失败', 400, False)

    return image


def images_to_video(images, fps=24, duration=10, size=(640, 480)):
    """
    多张图片合成视频

    :param images: 图片列表
    :param fps: 帧数
    :param duration: 持续时间
    :param size: 宽高（x, y）
    :return: 视频
    """

    imgs_url = images or []

    if len(imgs_url) == 0:
        return custom_response('没有图片链接', 400, False)

    videos = []

    for img_url in imgs_url:
        image = _url_to_image(img_url)
        video = ImageClip(np.array(image), duration=duration/len(imgs_url))
        videos.append(video)

    result_video = concatenate_videoclips(videos).resize(size)

    font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], Fonts.DEFAULT_FONT_FAMILY, '.ttf')
    text_clip = TextClip('测试显示', font=font_path, fontsize=70, bg_color='black', color='white')
    text_clip = text_clip.set_pos('center').set_duration(2)

    video = CompositeVideoClip([result_video, text_clip])

    video.write_videofile('out_video.mp4', fps=fps)
