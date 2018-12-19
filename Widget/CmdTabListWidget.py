#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created by Tan.Xing
Created date: 2018/12/4
Last edited: 2018/12/5
'''

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QColor, QPixmap, QDrag, QPainter, QCursor, QFont
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand, QPushButton
from Util.SqlHelper import SQLHelper
from Config import Config

class CmdTabListWidget(QListWidget):
    # 可以往外拖的QListWidget
    def __init__(self, *args, **kwargs):
        super(QListWidget, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 不能编辑
        self.setEditTriggers(self.NoEditTriggers)
        # 开启拖功能
        self.setDragEnabled(False)
        # 只能往外拖
        # self.setDragDropMode(self.DragDrop)
        # 忽略放
        self.setDefaultDropAction(Qt.IgnoreAction)
        # ****重要的一句（作用是可以单选，多选。Ctrl、Shift多选，可从空白位置框选）****
        # ****不能用ExtendedSelection,因为它可以在选中item后继续框选会和拖拽冲突****
        # self.setSelectionMode(self.ContiguousSelection)
        # 设置从左到右、自动换行、依次排列
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        # item的间隔
        self.setSpacing(2)
        # 橡皮筋(用于框选效果)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        self.initItems()

    # 实现拖拽的时候预览效果图
    # 这里演示拼接所有的item截图(也可以自己写算法实现堆叠效果)
    def startDrag(self, supportedActions):
        items = self.selectedItems()
        drag = QDrag(self)
        mimeData = self.mimeData(items)
        # 由于QMimeData只能设置image、urls、str、bytes等等不方便
        # 这里添加一个额外的属性直接把item放进去,后面可以根据item取出数据
        mimeData.setProperty('myItems', items)
        drag.setMimeData(mimeData)
        pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        for item in items:
            rect = self.visualRect(self.indexFromItem(item))
            painter.drawPixmap(rect, self.viewport().grab(rect))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(QCursor.pos()))
        drag.exec_(supportedActions)

    def mousePressEvent(self, event):
        # 列表框点击事件,用于设置框选工具的开始位置
        super(CmdTabListWidget, self).mousePressEvent(event)
        if event.buttons() != Qt.LeftButton or self.itemAt(event.pos()):
            return
        self._rubberPos = event.pos()
        self._rubberBand.setGeometry(QRect(self._rubberPos, QSize()))
        self._rubberBand.show()


    def mouseReleaseEvent(self, event):
        # 列表框点击释放事件,用于隐藏框选工具
        super(CmdTabListWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()

    def mouseMoveEvent(self, event):
        # 列表框鼠标移动事件,用于设置框选工具的矩形范围
        super(CmdTabListWidget, self).mouseMoveEvent(event)
        if self._rubberPos:
            pos = event.pos()
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QRect(QPoint(min(lx, rx), min(ly, ry)), size))

    def makeItem(self, cmd):
        size = QSize(200, 40)
        item = QListWidgetItem(self)
        if cmd == '+':
            item.setTextAlignment(Qt.AlignCenter)
        # item.setData(Qt.Quer, cmd)  # 把颜色放进自定义的data里面
        else:
            cmd = Config.TAB_HEAD+cmd
        item.setSizeHint(size)
        item.setText(cmd)
        label = QLabel(self)  # 自定义控件
        # label.setMargin(0)  # 往内缩进2
        label.resize(size)
        label.adjustSize()
        label.setFont(QFont("Timers", 20, QFont.Bold));
        self.setItemWidget(item, label)

    def initItems(self):
        sql = SQLHelper()
        sql.creat_cmd_tab_table()
        names = sql.query_cmdtabs_value()
        if not names:
            sql.add_cmdtab_value('基本命令',-100)
            sql.add_cmdtab_value('+',10000)
            names = sql.query_cmdtabs_value()
        print(names)
        for name in names:
            self.makeItem(name)