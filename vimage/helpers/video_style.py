# -*- coding:utf-8 -*-
from vimage.constant import *


class GoodsVideoStyle:
    """
        商品信息视频样式
    """

    def __init__(self, post_data, style_id=0):
        """
        视频初始化

        :param post_data: 接收的数据
        :param style_id: 样式 id
        """

        self.data = post_data or {}    # 数据
        self.style_id = style_id    # 样式标识
        self.duration = self.data.get('duration', 10)    # 持续时间(s)
        self.fps = self.data.get('fps', 24)    # 默认帧率

        width = Size.GOODS_VIDEO_SIZE['width']
        height = Size.GOODS_VIDEO_SIZE['height']
        default_size = {'width': width, 'height': height}
        self.size = self.data.get('size', default_size)    # 尺寸

        self.contents = self.data.get('contents', [])    # 内容，包含图片和文字信息

    def get_contents_images(self):
        """
            获取内容数据中的图片信息
        """

        if self.contents is None:
            return

        for content_data in self.contents:
            if not content_data or 'images' not in content_data and 'videos' not in content_data:
                return

            images = content_data.get('images')
            texts = content_data.get('texts')
            videos = content_data.get('videos')

            return {'images': images, 'texts': texts, 'videos': videos}
