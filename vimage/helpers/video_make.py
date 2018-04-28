# -*- coding:utf-8 -*-
import io
import requests as req
from flask import current_app
from PIL import Image
import numpy as np
import imageio
imageio.plugins.ffmpeg.download()

from moviepy.editor import *
from vimage.constant import *
from vimage.helpers.image_tools import load_url_image
from vimage.helpers.video_style import MakeVideoStyle


class TextClipObject:
    """
        文字帧
    """

    def __init__(self, text_data=None):
        """
        初始化文字帧对象

        :param text_data: 文字样式数据
        """

        default_font_color = Colors.DEFAULT_FONT_COLOR['black']
        default_font_name = Fonts.DEFAULT_FONT_FAMILY
        default_font_size = Size.DEFAULT_FONT_SIZE
        default_duration = 1

        data = text_data or {}

        self.txt = data.get('txt')                                  # 要写入的文本的字符串
        self.size = data.get('size')                                # 图片的大小. method = 'label'，可以自动设置
        self.fps = data.get('fps')                                  # fps
        self.bg_color = data.get('bg_color', None)                  # 背景颜色. 使用 TextClip.list('color') 查看颜色名称
        self.color = data.get('color', default_font_color)          # 文字颜色
        self.font = data.get('font', default_font_name)             # 使用的字体名称
        self.font_size = data.get('font_size', default_font_size)   # 字体大小
        self.align = data.get('align', 'center')                    # 对齐方式. method = 'caption' 时生效
        self.transparent = data.get('transparent', True)            # 透明度
        self.method = data.get('method', 'label')                   # 类别. 'label'/'caption'
        self.duration = data.get('duration', default_duration)      # 持续时间 (s)
        self.position = data.get('position', ('center', 'top'))     # 位置. (x, y)

    def make_text_clip(self):
        """
            生成文字帧
        """

        font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], self.font, '.ttf')  # 字体路径

        text_clip = TextClip(txt=self.txt,
                             font=font_path,
                             fontsize=self.font_size,
                             color=self.color,
                             bg_color=self.bg_color,
                             align=self.align,
                             size=self.size,
                             transparent=self.transparent,
                             method=self.method)

        text_clip = text_clip.set_position(self.position, relative=True).set_duration(self.duration)

        return text_clip


class ImageClipObject:
    """
        图像帧
    """

    def __init__(self, image_data=None):
        """
        初始化图片对象

        :param image_data: 图片样式数据
        """

        default_duration = 1

        data = image_data or {}

        self.images = data.get('images')                        # 图片url
        self.is_mask = data.get('is_mask', False)               # 剪辑是否是蒙版
        self.transparent = data.get('transparent', True)        # 透明度
        self.from_alpha = data.get('from_alpha', False)         # 透明度为 True 时，设置 alpha
        self.duration = data.get('duration', default_duration)  # 持续时间 (s)
        self.size = data.get('size')                            # 尺寸
        self.fps = data.get('fps')                              # fps

    def make_image_clip(self):
        """
            生成图片帧
        """

        clips = []

        duration = self.duration/len(self.images)

        for image_url in self.images:
            img = load_url_image(image_url)

            clip = ImageClip(np.array(img),
                             ismask=self.is_mask,
                             transparent=self.transparent,
                             fromalpha=self.from_alpha,
                             duration=duration).resize(self.size)
            clips.append(clip)

        image_clip = concatenate_videoclips(clips)

        return image_clip


class ColorClipObject:
    """
        显示一个颜色帧
    """

    def __init__(self, color_data=None):
        """
        初始化一个颜色帧对象

        :param color_data: 颜色数据
        """

        data = color_data or {}

        self.size = data.get('size')            # 剪辑的大小（width, height）
        self.color = data.get('color')          # is_mask 为 False 时 RGB 颜色，True 时 0——1
        self.is_mask = data.get('is_mask')      # 是否用作蒙版
        self.duration = data.get('duration')    # 持续时间 (s)

        # 生成结果
        self.color_clip = self.make_color_clip()

    def make_color_clip(self):
        """
            生成颜色帧
        """

        color_clip = ColorClip(size=self.size,
                               ismask=self.is_mask,
                               color=self.color,
                               duration=self.duration)

        return color_clip


def _make_image_clip(image_data):
    """
        制作图片帧视频
    """

    image_clip = None

    for data in image_data:
        img_obj = ImageClipObject(data)
        image_clip = img_obj.make_image_clip()

    return image_clip


def _make_text_clip(text_data, img_clip, size):
    """
    制作文字帧视频

    :param text_data: 文字数据
    :param img_clip: 图片帧
    :param size: 尺寸
    :return: 文字图片合成后的视频
    """

    clips = [img_clip]

    for data in text_data:
        txt_obj = TextClipObject(data)
        txt_clip = txt_obj.make_text_clip()
        clips.append(txt_clip)

    text_clip = CompositeVideoClip(clips, size=size)

    return text_clip


class VideoMake:
    """
        生成视频
    """

    def __init__(self, post_data=None):
        """
        初始化视频生成对象

        :param post_data: 视频展示的数据
        """

        style_id = 1

        self.style_data = MakeVideoStyle(post_data, style_id).get_style_data()
        self.content = self.style_data.get('content')
        self.images = self.style_data.get('images')
        self.size = self.style_data.get('size')
        self.fps = self.style_data.get('fps')
        self.duration = self.style_data.get('duration')
        self.img_duration = self.style_data.get('img_duration')

    def make_video(self):
        """
            开始制作视频
        """

        clips = []

        start = 0

        # 拆分内容数据，单独生成每一帧（一组数据，包含图片、文字等）
        for index, content in enumerate(self.content):
            # 图片
            images = content.get('images')
            img_clip = _make_image_clip(images)

            texts = content.get('texts')
            txt_clip = _make_text_clip(texts, img_clip, self.size)

            clips.append(txt_clip.set_start(start).crossfadein(0.2))
            start += self.img_duration * len(self.images[index])

        video = CompositeVideoClip(clips)
        video.write_videofile('out.mp4', fps=self.fps)

        return {'message': '创建成功'}


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
    text_clip = text_clip.set_position('center').set_duration(2)

    # 合成视频文件输出
    video = CompositeVideoClip([result_video, text_clip], size=size)
    video.write_videofile('out_video.mp4', fps=fps)
