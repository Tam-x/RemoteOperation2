#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created by Tan.Xing
Created date: 2018/12/11
新建类
Last edited: 2018/12/11
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from Main.UiController import windowController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QWidget()

    mainWindow.setFixedSize(1170, 750)
    # mainWindow.setWindowOpacity(0.95)  # 设置窗口透明度
    # mainWindow.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
    ui = windowController(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
    pass