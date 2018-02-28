# -*- coding: utf-8 -*-

from flask_script import Command


class InitialSetting(Command):
    """
    Install initial data of system
    """

    def run(self):
        print('Initial system data!')