# -*- coding: utf-8 -*-


class Sensitive:
    """
        敏感信息过滤
    """

    def __init__(self, text=None, image=None):
        self.text = text or ''  # 需要检测的文字
        self.result_text = ''  # 过滤完毕的文字
        self.image = image  # 需要检测的图片
        self.sensitive_words = list()  # 敏感词列表

        self.loadSensitiveWords(path='sensitive_word.txt')

    def loadSensitiveWords(self, path):
        """
            加载敏感词库
        """

        with open(path, 'r') as file:
            for line in file.readlines():
                self.sensitive_words.append(line.strip())

    def filterWords(self):
        """
            过滤敏感词
        """

        self.result_text = self.text

        for word in self.sensitive_words:
            if word in self.result_text:
                self.result_text = self.result_text.replace(word, len(word) * '*')

        return self.result_text
