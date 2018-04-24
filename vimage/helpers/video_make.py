# -*- coding:utf-8 -*-
import io
import requests as req
from flask import current_app
from PIL import Image
import numpy as np
import imageio
imageio.plugins.ffmpeg.download()

from moviepy.editor import *
from vimage.constant import Fonts
from vimage.helpers.image_tools import load_url_image


def images_to_video(images, fps=24, duration=10, size=(640, 480)):
    """
    多张图片合成视频

    :param images: 图片列表
    :param fps: 帧数
    :param duration: 持续时间
    :param size: 宽高（x, y）
    :return: 视频
    """

    images_url = images or []

    videos = []

    # 图像帧
    for img_url in images_url:
        image = load_url_image(img_url)
        clip = ImageClip(np.array(image), duration=duration/len(images_url)).set_start(1.5).crossfadein(0.5)
        clip = clip.resize(size)
        videos.append(clip)

    # 图像合成视频
    result_video = concatenate_videoclips(videos)

    # 文字帧
    font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], Fonts.DEFAULT_FONT_FAMILY, '.ttf')
    text_clip = TextClip('测试显示', font=font_path, fontsize=70, color='white', method='label')
    text_clip = text_clip.set_pos('center').set_duration(2)

    # 合成视频文件输出
    video = CompositeVideoClip([result_video, text_clip], size=size)
    video.write_videofile('out_video.mp4', fps=fps)


class VideoMake(object):
    """
        视频生成器
    """

    def __int__(self, data):
        """
        初始化视频对象

        :param data: 视频数据
        """
