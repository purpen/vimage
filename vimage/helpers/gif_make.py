# -*- coding: utf-8 -*-
import requests as req
from PIL import Image, ImageSequence
from io import BytesIO
from vimage.helpers.utils import *

from flask import current_app
from vimage.helpers import QiniuCloud, QiniuError
from vimage.constant import *


def _download_image(url, is_convert=False):
    """
    从图片链接中下载图片

    :param url: 链接
    :param is_convert: 图片是否转换
    :return: 图片
    """

    try:
        r = req.get(url)
        image = Image.open(BytesIO(r.content))

        if is_convert is True:
            image = image.convert('RGBA')

    except (req.exceptions.HTTPError, req.exceptions.URLRequired):
        return custom_response('图片链接获取失败', 400, False)

    return image


def _qiniu_upload(content, folder, key):
    """
    上传图片至云服务

    :param content: 上传的数据
    :param key: path key
    :return: 上传结果
    """

    folder = folder
    path_key = '%s/%s' % (folder, key)

    # 保存的地址
    result_url = 'https://%s/%s' % (current_app.config['CDN_DOMAIN'], path_key)

    qiniu_cloud = QiniuCloud(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_ACCESS_SECRET'],
                             current_app.config['QINIU_BUCKET_NAME'])
    try:
        qiniu_cloud.upload_content(content, path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload file error: %s' % str(err))

    return result_url


def scale_image_size(image, scale_w=None, scale_h=None):
    """
    按比列缩放图片的尺寸

    :param image: 图片
    :param scale_w: 按宽度
    :param scale_h: 按高度
    :return: 缩放后的尺寸
    """

    img_w, img_h = image.size[0], image.size[1]

    if scale_w is not None:
        img_h = scale_w / img_w * img_h
        size = (scale_w, int(img_h))

        return size

    elif scale_h is not None:
        img_w = img_h / scale_h * img_w

        size = (int(img_w), scale_h)

        return size

    return image.size


class GifTool:
    """
        GIF图制作工具
    """

    def __init__(self, type, images, video=None, gif=None, size=None, duration=None):
        """
        初始化 GIF 图类别

        :param type: 类型 1：图片合成GIF、2：视频制作GIF、3：GIF 提取帧图片、4：GIF 倒放 | (默认为 1)
        :param images: 每帧图片的集合
        :param video: 视频地址
        :param gif: GIF 图地址
        :param size: 尺寸
        :param duration: 持续时间 ms
        """

        self.type = type or 1
        self.images = images
        self.video = video
        self.gif = gif
        self.size = size
        self.duration = duration or 500

        self.tools = {
            '1': self.create_images_gif(),
            '3': self.create_resolve_gif(),
            '4': self.create_reverse_gif()
        }

    def create_images_gif(self):
        """
            多张图片合成 GIF 图
        """

        if self.images is None or self.type != 1:
            return

        images = []

        # 默认图片
        default_image = _download_image(self.images[0], True)

        for image_url in self.images:
            image = self.resize_image(_download_image(image_url, True), default_image.size)
            images.append(image)

        # GIF 图的二进制流
        gif_content = BytesIO()
        images[0].save(gif_content, 'gif', save_all=True, append_images=images[1:], duration=self.duration, loop=0)

        result = _qiniu_upload(gif_content.getvalue(), 'gif', QiniuCloud.gen_path_key('.gif'))

        return {
            'result_gif': result
        }

    def create_resolve_gif(self):
        """
            分解 GIF 图为单张图片
        """

        if self.gif is None or self.type != 3:
            return

        original_gif = _download_image(self.gif)

        images = []

        # GIF图片流的迭代器
        for iter in ImageSequence.Iterator(original_gif):
            image_content = BytesIO()

            image = self.resize_image(iter.copy())
            image.save(image_content, 'png')

            result = _qiniu_upload(image_content.getvalue(), 'gif', QiniuCloud.gen_path_key())
            images.append(result)

        return {
            'gif': self.gif,
            'images': images
        }

    def create_reverse_gif(self):
        """
            GIF 图倒放
        """

        if self.gif is None or self.type != 4:
            return

        original_gif = _download_image(self.gif)

        images = []

        # GIF图片流的迭代器
        for iter in ImageSequence.Iterator(original_gif):
            image = self.resize_image(iter.copy())
            images.append(image)

        # 倒序排列
        images.reverse()

        # GIF 图的二进制流
        gif_content = BytesIO()
        images[0].save(gif_content, 'gif', save_all=True, append_images=images[1:], duration=self.duration, loop=0)

        result = _qiniu_upload(gif_content.getvalue(), 'gif', QiniuCloud.gen_path_key('.gif'))

        return {
            'gif': self.gif,
            'result_gif': result
        }

    def get_result_gif(self):
        """
        获取 GIF 制作的结果

        :return: 结果数据
        """

        tool_type = str(self.type)
        result = self.tools.get(tool_type)

        return result

    def create_gif_poster(self, info_image):
        """
        制作动态海报

        :param info_image: 海报展示的内容图片
        :return: GIF 海报
        """

        images = []

        poster_width = info_image.size[0]

        for image_url in self.images:
            # 动态图片
            image = _download_image(image_url, True)
            image = image.resize(scale_image_size(image, poster_width, None))

            # 动态图片粘贴到空白画布（调整海报样式所需大小）
            canva = Image.new('RGBA', info_image.size, Colors.DEFAULT_BACKGROUND_COLOR['white'])
            canva.paste(image, (0, 0), image)

            # 调整后的每帧图片，拼贴展示信息
            canva.paste(info_image, (0, 0), info_image)

            images.append(canva)

        # GIF 图的二进制流
        gif_content = BytesIO()
        images[0].save(gif_content, 'gif', save_all=True, append_images=images[1:], duration=self.duration, loop=0)

        result = _qiniu_upload(gif_content.getvalue(), 'gif', QiniuCloud.gen_path_key('.gif'))

        return {
            'gif_poster': result
        }

    def resize_image(self, image, default_size=None):
        """
        调整 GIF 图片的尺寸

        :param image: 图片
        :param default_size: 默认尺寸
        :return: 调整后的图片
        """

        if self.size is None and default_size is None:
            return image

        size = self.size or default_size
        result_image = image.resize(size, Image.ANTIALIAS)

        return result_image
