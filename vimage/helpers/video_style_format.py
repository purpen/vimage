# -*- coding: utf-8 -*-


def format_image_data(images, size, fps, is_mask, transparent, from_alpha, duration):
    """
    格式化图片样式数据

    :param images: 图片
    :param size: 尺寸
    :param fps: 帧率
    :param is_mask: 是否是遮罩
    :param transparent: 透明度
    :param from_alpha: 透明数值
    :param duration: 持续时间
    :return: 样式数据
    """

    image_data = {
        'images': images,
        'size': size,
        'fps': fps,
        'is_mask': is_mask,
        'transparent': transparent,
        'from_alpha': from_alpha,
        'duration': duration
    }

    return image_data


def format_text_data(texts, size, fps, color, bg_color, font, font_size, position, method, align, transparent, duration):
    """
    格式化文字样式数据

    :param texts: 文本
    :param size: 图片的大小. method = 'label'，可以自动设置
    :param fps: 帧率
    :param color: 文字颜色
    :param bg_color: 背景颜色
    :param font: 字体名称
    :param font_size: 字体大小
    :param position: 位置. (x, y)
    :param method: 类别. 'label'/'caption'
    :param align: 对齐方式. method = 'caption' 时生效
    :param transparent: 透明度
    :param duration: 持续时间 (s)
    :return: 样式数据
    """

    text_data = {
        'txt': texts,
        'size': size,
        'fps': fps,
        'color': color,
        'bg_color': bg_color,
        'font': font,
        'font_size': font_size,
        'position': position,
        'method': method,
        'align': align,
        'transparent': transparent,
        'duration': duration
    }

    return text_data


def format_audio_data(filename, duration, buffersize=200000, nbytes=2, bitrate=3000, fps=44100):
    """
    格式化音频结果数据

    :param filename: 展示内容
    :param duration: 持续时间
    :param buffersize: 缓冲区大小
    :param nbytes: 原始音频文件每帧的位数. 采样宽度（对于16位声音设置为2，对于32位声音设置为4）
    :param bitrate: 比特率
    :param fps: 音频文件中每秒的帧数
    :return: 样式数据
    """

    result_data = {
        'filename': filename,
        'duration': duration,
        'buffersize': buffersize,
        'nbytes': nbytes,
        'bitrate': bitrate,
        'fps': fps
    }

    return result_data


def format_result_data(content, audio, images, size, fps, duration, img_duration):
    """
    格式化视频结果数据

    :param content: 展示内容
    :param audio: 音频信息
    :param images: 所有图片
    :param size: 尺寸
    :param fps: 帧率
    :param duration: 持续时间
    :param img_duration: 单张图片持续时间
    :return: 样式数据
    """

    result_data = {
        'content': content,
        'audio': audio,
        'images': images,
        'size': size,
        'fps': fps,
        'duration': duration,
        'img_duration': img_duration
    }

    return result_data
