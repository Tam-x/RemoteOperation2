#!/usr/bin/python

# -*- coding: utf-8 -*-

from __future__ import division
from PyQt5 import QtGui, QtCore, QtWidgets

class CmdInPutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setFixedSize(350, 120)
        self.setWindowTitle('快捷命令输入')
        grid = QtWidgets.QGridLayout()
        self.lab1 = QtWidgets.QLabel('快捷名称:', parent=self)
        self.lab2 = QtWidgets.QLabel('指令内容:', parent=self)
        grid.addWidget(self.lab1, 0, 0, 1, 1)
        self.num_R = QtWidgets.QLineEdit(parent=self)
        grid.addWidget(self.num_R, 0, 1, 1, 1)
        grid.addWidget(self.lab2, 1, 0, 1, 1)
        self.num_C = QtWidgets.QLineEdit(parent=self)
        grid.addWidget(self.num_C, 1, 1, 1, 1)
        buttonBox = QtWidgets.QDialogButtonBox(parent=self)
        buttonBox.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平方向
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)  # 确定和取消两个按钮
        buttonBox.accepted.connect(self.accept)  # 确定
        buttonBox.rejected.connect(self.reject)  # 取消
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        spacerItem = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        def closeEvent(self, event):
            reply = QtWidgets.QMessageBox.question(self, 'Close Message',
                                               "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
