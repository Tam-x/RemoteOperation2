#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created by Tan.Xing
Created date: 2018/12/3
实现服务/命令简单解析
edited: 2018/12/5
数据写入数据库
Last edited: 2018/12/5
'''

from Util.SqlHelper import SQLHelper
from Util import LogInfo

'''
解析后的服务配置数据写入数据库
'''
def parseServerInfo(info):
    if info:
        try:
            infos = info.split('|')
            if len(infos)==5:
                sql = SQLHelper()
                name = infos[0]
                ip = infos[1]
                account = infos[2]
                pwd = infos[3]
                port = infos[4]
                if(len(pwd) == 256):
                    sql.add_server_value(name,ip, account,pwd, port)
        except Exception as e:
            LogInfo.put(e.args)
            pass

def parserCmdInfo(info,index, type):
    if info:
        try:
            infos = info.split('=')
            if len(infos)==2:
                sql = SQLHelper()
                name = infos[0]
                cmd = infos[1]
                sql.add_cmd_value(name,cmd, type, index)
        except Exception as e:
            LogInfo.put(e.args)
            pass

def parseCmdTabInfo(info, index):
    if info:
        try:
            name = info.strip()
            if name:
                sql = SQLHelper()
                sql.add_cmdtab_value(name,index)
        except Exception as e:
            LogInfo.put(e.args)
            pass

