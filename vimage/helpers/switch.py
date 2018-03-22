# -*- coding: utf-8 -*-


class Switch(object):
    """
        switch..case..
    """

    def __init__(self, value):
        self.value = value
        self.fail = False

    def match(self, *args):
        """
            匹配方法
        """

        if self.fail or not args:
            return True

        elif self.value in args:
            self.fail = True
            return True

        else:
            return False

    def __iter__(self):
        yield self.match
        raise StopIteration
