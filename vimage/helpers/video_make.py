# -*- coding:utf-8 -*-
import io
import requests as req
from flask import current_app
from PIL import Image
import numpy as np
import imageio

imageio.plugins.ffmpeg.download()

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
from vimage.constant import *
from vimage.helpers.image_tools import load_url_image
from vimage.helpers.video_style import MakeVideoStyle
from vimage.helpers.utils import timestamp, MixGenId
from PIL import Image


def animation_vortex(screen_pos, i, n_letters):
    """
        文字加载动画一: 漩涡
    """

    # 矩阵转换
    def rotMatrix(a):
        return np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])

    # 运动的角度
    angle = i * np.pi / n_letters
    v = rotMatrix(angle).dot([-1, 0])

    if i % 2:
        v[1] = -v[1]

    # 阻尼
    def damp(t):
        return 1.0 / (0.3 + t ** 8)

    return lambda t: screen_pos + 400 * damp(t) * rotMatrix(0.5 * damp(t) * angle).dot(v)


def animation_cascade(screen_pos, i, n_letters=None):
    """
        文字加载动画二:  下坠
    """

    v = np.array([0, -1])

    def damp(t):
        return 1 if t < 0 else abs(np.sinc(t) / (1 + t ** 4))

    return lambda t: screen_pos + v * 400 * damp(t - 0.15 * i)


def animation_arrive(screen_pos, i, n_letters=None):
    """
        文字加载动画三: 右进
    """

    v = np.array([-1, 0])

    def damp(t):
        return max(0, 3 - 3 * t)

    return lambda t: screen_pos - 400 * v * damp(t - 0.2 * i)


def move_letters(func_pos, letters):
    """
        移动文字，形成动画
    """

    return [letter.set_position(func_pos(letter.screenpos, i, len(letters)))
            for i, letter in enumerate(letters)]


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

        data = text_data or {}

        self.txt = data.get('txt')  # 要写入的文本的字符串
        self.size = data.get('size')  # 图片的大小. method = 'label'，可以自动设置
        self.fps = data.get('fps')  # fps
        self.bg_color = data.get('bg_color', None)  # 背景颜色. 使用 TextClip.list('color') 查看颜色名称
        self.color = data.get('color', default_font_color)  # 文字颜色
        self.font = data.get('font', default_font_name)  # 使用的字体名称
        self.font_size = data.get('font_size', default_font_size)  # 字体大小
        self.align = data.get('align', 'center')  # 对齐方式. method = 'caption' 时生效
        self.transparent = data.get('transparent', True)  # 透明度
        self.method = data.get('method', 'label')  # 类别. 'label'/'caption'
        self.duration = data.get('duration')  # 持续时间 (s)
        self.position = data.get('position', ('center', 'top'))  # 位置. (x, y)

    def make_text_clip(self):
        """
            生成文字帧
        """

        font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], self.font, '.ttf')

        txt_clip = TextClip(txt=self.txt,
                            font=font_path,
                            fontsize=self.font_size,
                            color=self.color,
                            bg_color=self.bg_color,
                            align=self.align,
                            size=None,
                            transparent=self.transparent,
                            method=self.method).set_position(self.position).set_duration(self.duration)

        # text_clip = CompositeVideoClip([txt_clip], size=self.size)

        """
        生成文字动画
        每个单独对象的 ImageClips 列表
        
        :param rem_thr: 值的大小，影响汉字的偏旁部首显示
        """
        # letters = findObjects(text_clip, rem_thr=1)
        #
        # clips = CompositeVideoClip(move_letters(animation_arrive, letters), size=self.size).set_duration(self.duration)

        # clips.write_videofile(('txt_%s.avi' % MixGenId.gen_letters()), fps=self.fps, codec='mpeg4')

        return txt_clip


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

        self.images = data.get('images')  # 图片url
        self.is_mask = data.get('is_mask', False)  # 剪辑是否是蒙版
        self.transparent = data.get('transparent', True)  # 透明度
        self.from_alpha = data.get('from_alpha', False)  # 透明度为 True 时，设置 alpha
        self.duration = data.get('duration', default_duration)  # 持续时间 (s)
        self.size = data.get('size')  # 尺寸
        self.fps = data.get('fps')  # fps

    def make_image_clip(self):
        """
            生成图片帧
        """

        clips = []

        duration = self.duration / len(self.images)

        for image_url in self.images:
            img = load_url_image(image_url).resize(self.size)

            clip = ImageClip(np.array(img),
                             ismask=self.is_mask,
                             transparent=self.transparent,
                             fromalpha=self.from_alpha,
                             duration=duration)
            clips.append(clip)

        image_clip = concatenate_videoclips(clips)

        return image_clip


class AudioClipObject:
    """
        音频对象
    """

    def __init__(self, audio_data=None):
        """
        初始化一个音频

        :param audio_data: 音频数据
        """

        data = audio_data or {}

        self.filename = data.get('filename')
        self.duration = data.get('duration')
        self.buffersize = data.get('buffersize')
        self.nbytes = data.get('nbytes')
        self.bitrate = data.get('bitrate')
        self.fps = data.get('fps')

    def make_audio_clip(self):
        """
            生成音频剪辑
        """

        # 音频文件地址
        audio_path = '%s%s%s' % (current_app.config['MAKE_VIDEO_AUDIO_PATH'], self.filename, '.mp3')

        audio = AudioFileClip(filename=audio_path,
                              buffersize=self.buffersize,
                              nbytes=self.nbytes,
                              fps=self.fps).set_duration(self.duration)

        return audio


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

        self.size = data.get('size')  # 剪辑的大小（width, height）
        self.color = data.get('color')  # is_mask 为 False 时 RGB 颜色，True 时 0——1
        self.is_mask = data.get('is_mask')  # 是否用作蒙版
        self.duration = data.get('duration')  # 持续时间 (s)

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
        self.audio = self.style_data.get('audio')
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

        # 每段视频开始的时间，切换时渐隐效果
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

        # 音频剪辑
        audio = AudioClipObject(self.audio).make_audio_clip()
        # 最终剪辑文件
        video = CompositeVideoClip(clips, size=self.size).set_audio(audio)

        video.write_videofile('out.mp4', fps=self.fps)

        return {'message': '创建成功'}
