# -*- coding: utf-8 -*-

<<<<<<< HEAD
import json
from flask_script import Command

from config import basedir
from vimage.models import Sensitive
from vimage import db


def load_data(filename):
    """加载json格式数据"""

    try:
        with open(filename, 'r', encoding="utf-8") as f:
            result = json.load(f)
            return result
    except Exception as err:
        print('读取文件异常: %s' % str(err))
        return {}


class InitialSystem(object):
    """系统初始化，配置系统默认数据"""

    @staticmethod
    def init_sensitives():
        """初始化敏感词汇"""

        records = load_data(basedir + '/commands/sensitives.json')
        for record in records:
            word = record['word']
            type = record['type']

            sensitive = Sensitive.query.filter_by(word=word, type=type).first()
            if sensitive:
                print(f'System sensitive: {word} already initial, exit!')
                continue

            # 保存敏感词汇
            sensitive = Sensitive()
            sensitive.word = word
            sensitive.type = type
            db.session.add(sensitive)

        db.session.commit()

        print('System sensitive is initial!')

=======
from flask_script import Command

>>>>>>> a42c3763e1a6b24bef1e39b34212f2a744444c6b

class InitialSetting(Command):
    """
    Install initial data of system
    """

    def run(self):
<<<<<<< HEAD
        print('Begin Initial system data!')

        # 初始化敏感词汇
        InitialSystem.init_sensitives()

        print('End Initial system data!')
=======
        print('Initial system data!')
>>>>>>> a42c3763e1a6b24bef1e39b34212f2a744444c6b
