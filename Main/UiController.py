#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created by Tan.Xing
Created date: 2018/12/3
Last edited: 2018/12/6
'''
from PyQt5.QtWidgets import QDialog, QDirModel, QFileDialog,QMenu,QAction
from PyQt5.QtCore import QDir, QPoint,Qt
from PyQt5.QtGui import QCursor,QPalette
from UI.UI import Ui_Form
from Util.SqlHelper import SQLHelper
from Util.LogInfo import *
from Util.CfgChecker import *
from Util.RemoteHelper import RemoteHelper
from Util.RSAHelper import *
from Widget.CmdInputDialog import CmdInPutDialog
from PyQt5.QtCore import QTimer
from Res.QssStyle import *
import re, threading

class windowController(Ui_Form, QDialog):
    def __init__(self, widge):
        super(windowController, self).__init__()
        self.setupUi(widge)
        self.init()

    def init(self):
        self.current_ssh = None
        self.channel = None
        self.isConnected = False
        self.currentServer = None
        self.currentUser = None
        self.currentPwd = None
        self.cmdSendLen = 0
        self.currentTabName = '基本命令'
        self.light_index = 0
        self.sql = SQLHelper()
        self.timer = QTimer()
        self.lightTimer = QTimer()
        self.queue = Log()
        self.timer.start(10)
        self.sql.creat_cmd_table()
        self.sql.creat_cmd_tab_table()
        self.sql.creat_server_table()
        self.model = QDirModel(self)
        self.model.setReadOnly(False)
        self.model.setSorting(QDir.Name | QDir.IgnoreCase)

        self.listWidget_2.itemClicked.connect(self.click_list_item)
        self.listWidget.itemClicked.connect(self.click_listtab_item)
        self.toolButton.clicked.connect(lambda: self.open_file(1))
        self.toolButton_2.clicked.connect(lambda: self.open_file(2))
        self.toolButton_8.clicked.connect(lambda :self.open_file(3))
        self.toolButton_5.clicked.connect(self.click_visit_btn)
        self.toolButton_3.clicked.connect(self.clean_log)
        self.toolButton_6.clicked.connect(self.click_rsa_btn)
        self.pushButton_5.clicked.connect(self.click_connect_btn)
        self.pushButton_6.clicked.connect(self.click_upload_file_btn)
        self.pushButton_7.clicked.connect(self.click_download_file_btn)
        self.pushButton_9.clicked.connect(self.click_ssh_change_btn)
        self.listWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_2.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)

        self.timer.timeout.connect(self.show_log)
        self.lightTimer.timeout.connect(self.run_light)
        self.comboBox.addItems(self.sql.query_servers_value())
        self.listWidget.setStyleSheet(list_tab_style)
        self.listWidget_2.setStyleSheet(list_cmd_style)

    def run_up_thread(self):
        t = threading.Thread(target=self.remoteHelper.upload,args=(self.lineEdit.text(), self.lineEdit_2.text()))
        t.start()

    def run_down_thread(self):
        t = threading.Thread(target=self.remoteHelper.download_files, args=(self.lineEdit.text(), self.lineEdit_2.text()))
        t.start()


    def show_info(self):
        index = self.treeView.currentIndex()
        file_name = self.model.fileName(index)
        file_path = self.model.filePath(index)
        self.lineEdit.setText(file_path)

    def click_add_list_item(self, item, type):
        dialog = CmdInPutDialog()
        dialog.setAutoFillBackground(True)
        # pal = QPalette()
        # pal.setColor(QPalette.Background, Qt.black)
        # dialog.setPalette(pal)
        if type is not 1:
            dialog.lab2.setText('分组优先级')
        if dialog.exec_():
            hs = dialog.num_R.text()
            ls = dialog.num_C.text()
            if hs and ls:
                try:
                    if type == 1:
                        self.sql.add_cmd_value(hs, ls, self.currentTabName,self.listWidget_2.count()+1)
                        self.listWidget_2.clear()
                        for name in self.sql.query_cmds_value(self.currentTabName):
                            self.listWidget_2.makeItem(name)
                    else:
                        self.sql.add_cmdtab_value(hs, ls);
                        self.listWidget.clear()
                        for name in self.sql.query_cmdtabs_value():
                            self.listWidget.makeItem(name)
                except:
                    self.textBrowser.append('添加命令失败！')

    def click_list_item(self, item):
        if item.text() == '+':
            self.click_add_list_item(item, 1)
            return
        if not self.isConnected:
            return
        cmd = self.sql.query_cmd_value(item.text())
        if cmd and self.channel:
            self.cmdSendLen = len(cmd)
            self.channel.send(cmd+'\n')

    def click_listtab_item(self, item):
        if item.text() == '+':
            self.click_add_list_item(item, 2)
            return
        if not self.currentTabName == item.text()[3:]:
            self.currentTabName = item.text()[3:]
            self.update_cmd_list(self.currentTabName)

    def myListWidgetContext(self, point):
        if self.listWidget_2.itemAt(self.listWidget_2.mapFromGlobal(QCursor.pos())) and\
            not self.listWidget_2.currentItem().text() == '+':
            popMenu = QMenu()
            changeaction = QAction(u'取消', self)
            deleaction = QAction(u'删除', self)
            popMenu.addAction(changeaction)
            popMenu.addAction(deleaction)
            deleaction.triggered.connect(lambda :self.delete_cmd_button(self.listWidget_2.currentItem().text()))
            popMenu.setStyleSheet(list_cmd_menu_style)
            popMenu.exec_(QCursor.pos())

    def click_listwidget_tab(self, point):
        if self.listWidget.itemAt(self.listWidget.mapFromGlobal(QCursor.pos())) and\
            not self.listWidget.currentItem().text() == '+':
            popMenu = QMenu()
            changeaction = QAction(u'修改', self)
            deleaction = QAction(u'删除', self)
            popMenu.addAction(changeaction)
            popMenu.addAction(deleaction)
            deleaction.triggered.connect(lambda :self.delete_cmd_button(self.listWidget_2.currentItem().text()))
            popMenu.setStyleSheet(
            "QMenu{\
            background-color: gray; /* sets background of the menu 设置整个菜单区域的背景色，我用的是白色：white*/\
            border: 1px solid white;/*整个菜单区域的边框粗细、样式、颜色*/\
        }\
        QMenu#item {\
            /* sets background of menu item. set this to something non-transparent\
                if you want menu color and menu item color to be different */\
            background-color: transparent;\
            padding:8px 32px;/*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/\
            margin:0px 8px;/*设置菜单项的外边距*/\
            border-bottom:1px solid #DBDBDB;/*为菜单项之间添加横线间隔*/\
        }\
        QMenu#item:selected { /* when user selects item using mouse or keyboard */\
            background-color: #2dabf9;/*这一句是设置菜单项鼠标经过选中的样式*/\
        }")
            popMenu.exec_(QCursor.pos())


    '''
    import configure from file
    if True means server or False cmd
    '''
    def open_file(self, flag):
        fileName = QFileDialog.getOpenFileName(caption='选择文件')
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        result = False
        if fileName:
            try:
                self.textBrowser.append('导入配置：\n')
                index = 0
                name = self.currentTabName
                for line in open(fileName[0],encoding='gbk',errors='ignore'):
                    if '#' not in line and line.strip():
                        self.textBrowser.append(line)
                        index += 1
                        if flag == 1:
                            self.import_server_cfg(line)
                        elif flag == 2:
                            index += self.listWidget_2.count()
                            self.import_cmd_cfg(line, index, name)
                        else:
                            index += self.listWidget.count()
                            self.import_cmdtab_cfg(line, index)
                        result = True
                if result:
                    if flag == 1:
                        self.update_server_list()
                    elif flag == 2:
                        self.update_cmd_list(name)
                    else:
                        self.update_cmdtab_list()
            except Exception as e:
                LogInfo.put((e.args))

    def delete_cmd_button(self, name):
        self.sql.delete_cmd_value(name)
        item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
        item = None

    def import_server_cfg(self, info):
        parseServerInfo(info)

    def import_cmdtab_cfg(self, info, index):
        parseCmdTabInfo(info, index)

    def import_cmd_cfg(self, info, index, type):
        parserCmdInfo(info, index, type)

    def update_server_list(self):
        self.comboBox.clear()
        self.comboBox.addItems(self.sql.query_servers_value())

    def update_cmd_list(self, type):
        self.listWidget_2.clear()
        names = self.sql.query_cmds_value(type)
        for name in names:
            self.listWidget_2.makeItem(name)

    def update_cmdtab_list(self):
        self.listWidget.clear()
        names = self.sql.query_cmdtabs_value()
        for name in names:
            self.listWidget.makeItem(name)

    def click_upload_file_btn(self):
        if self.isConnected and self.lineEdit.text() and self.lineEdit_2.text():
            try:
                self.pushButton_6.setEnabled(False)
                self.run_up_thread()
            except Exception as e:
                self.queue.get_queue().put(e.args)
                self.pushButton_6.setEnabled(True)


    def click_download_file_btn(self):
        if self.isConnected and self.lineEdit.text() and self.lineEdit_2.text():
            try:
                self.pushButton_7.setCheckable(False)
                self.run_down_thread()
            except Exception as e:
                self.queue.get_queue().put(e.args)
                self.pushButton_7.setEnabled(True)

    def click_connect_btn(self):
        if self.isConnected:
            self.pushButton_5.setText('连接')
            self.isConnected = False
            try:
                self.ssh.close()
            except:
                pass
            self.lightTimer.stop()
        else:
            try:
                if self.comboBox.count() < 1:
                    return
                infos = self.sql.query_server_value(self.comboBox.currentText())
                self.lightTimer.start(250)
                t = threading.Thread(target=self.connect_remote, args=(infos,))
                t.start()
                self.pushButton_5.setText('断开')
            except:
                if self.lightTimer.isActive():
                    self.lightTimer.stop()
                    try:
                        self.ssh.close()
                    except:
                        pass
                self.pushButton_7.setText('连接')
                self.isConnected = False

    def connect_remote(self, infos):
        if(self.comboBox.count()>0):
            if infos:
                try:
                    code = decrypt_msg(infos[3])
                except Exception as e:
                    LogInfo.put(e.args)
                    return
                arg = {'ip': infos[1], 'user': infos[2], 'password': code, 'port': 22}
                self.currentServer = infos[1]
                self.currentUser = infos[2]
                self.currentPwd = code
                self.remoteHelper = RemoteHelper(arg)
                tmpstr = u'开始连接...用户名:' + self.currentUser + u'  密码:******' + ' IP:' + self.currentServer
                LogInfo.put(tmpstr)
                self.remoteHelper.startup()
                import paramiko
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.currentServer, port=22, username=self.currentUser, password=self.currentPwd, compress=True)
                # 建立交互式shell连接
                self.isConnected = True
                self.channel = self.ssh.invoke_shell()
                self.windows_shell(self.channel)

    def show_log(self):
        while not self.queue.get_queue().empty():
            strs = str(self.queue.get_queue().get())
            if strs == '--download over--':
                self.pushButton_7.setEnabled(True)
            if strs.__contains__('upload'):
                self.pushButton_6.setEnabled(True)
            self.textBrowser.append(strs)

    def run_light(self):
        styles = [red_light_style, green_light_style, yellow_light_style]
        if(self.light_index > 2):
            self.light_index = 0
        self.pushButton.setStyleSheet(styles[self.light_index])
        self.light_index += 1
        if (self.light_index > 2):
            self.light_index = 0
        self.pushButton_2.setStyleSheet(styles[self.light_index])
        self.light_index += 1
        if (self.light_index > 2):
            self.light_index = 0
        self.pushButton_3.setStyleSheet(styles[self.light_index])

    def click_visit_btn(self):
        import webbrowser
        url = 'www.yarlungsoft.com'
        webbrowser.open(url, new=0, autoraise=True)

    def clean_log(self):
        self.textBrowser.clear()

    def click_ssh_change_btn(self):
        cmd = str(self.lineEdit_3.text())
        if cmd and self.channel and self.isConnected:
            self.channel.send(cmd+'\n')
            self.cmdSendLen = len(cmd)
            LogInfo.put(cmd)

    def windows_shell(self, chan):
        import sys
        import threading
        # sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        def writeall(sock):
            while True:
                data = sock.recv(256)
                if not data:
                    sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                    sys.stdout.flush()
                    LogInfo.put('\r\n当前连接已经断开！！！\r\n')
                    break
                sys.stdout.write(data.decode('gbk'))
                try:
                    sys.stdout.flush()
                except Exception as e:
                    print(e.args)
                    pass
                self.cmdSendLen -= len(str(data.decode('gb2312','ignore')).strip())
                if(self.cmdSendLen < 0):
                    LogInfo.put(data.decode('gb18030','ignore'))

        writer = threading.Thread(target=writeall, args=(chan,))
        writer.start()

    def click_rsa_btn(self):
        dialog = CmdInPutDialog()
        dialog.setWindowTitle('安全加密')
        dialog.setAutoFillBackground(True)
        dialog.lab1.setText('输入您的密码')
        dialog.lab2.setHidden(True)
        dialog.num_C.setHidden(True)
        if dialog.exec_():
            hs = dialog.num_R.text().strip()
            if hs:
                encrypted_msg(hs)

