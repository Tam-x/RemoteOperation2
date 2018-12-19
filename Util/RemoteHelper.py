# -*- coding:utf-8 -*-
import paramiko
import os
from Util import LogInfo

_XFER_FILE = 'FILE'
_XFER_DIR  = 'DIR'

class RemoteHelper(object):
    def __init__(self, arg):
        super(RemoteHelper, self).__init__()
        # 赋值参数[字典]
        # 参数格式 arg = {'ip':'填ip','user':'用户名','password':'密码','port':22}
        self.arg = arg
        # 赋值参数[FTP]
        self.sftp = None

    # 启动程序
    def startup(self):
        # 连接FTP
        if self.sftp != None:
            print( u'您已经成功连接了')
        tmpstr = u'开始连接...用户名:'+self.arg['user']+u'  密码:'+self.arg['password']+' IP:'+self.arg['ip']+u' 端口:'+str(self.arg['port'])
        # LogInfo.put(tmpstr)
        transport = paramiko.Transport((self.arg['ip'], self.arg['port']))
        transport.connect(username=self.arg['user'], password=self.arg['password'])
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        # LogInfo.put(u'sftp连接成功 '+self.arg['ip'])

    # 关闭程序
    def shutdown(self):
        # 关闭FTP
        if self.sftp:
            self.sftp.close()
            LogInfo.put('### disconnect sftp server: %s!'%self.arg['ip'])
            self.sftp = None

    # 处理上传
    def upload(self, source, target, replace=False):
        ### 操作数据
        # 来源路径
        if self.sftp is None:
            return
        source = source.replace('\\', '/')
        # 目标路径
        target = target.replace('\\', '/')

        ### 验证数据
        if not os.path.exists(source):
            LogInfo.put(u'来源资源不存在，请检查：' + source)
            return
        ### 格式数据
        # 格式化目标路径
        self.__makePath(target)

        ### 处理数据
        # 文件媒体数据(文件类型, 文件名称)
        filetype, filename = self.__filetype(source)
        # 判断文件类型
        if filetype == _XFER_DIR:
            # 1.目录
            self.uploadDir(source, target, replace)
        elif filetype == _XFER_FILE:
            # 2.文件
            self.uploadFile(source, filename, replace)
        LogInfo.put('--upload over--')


    # 传送目录
    def uploadDir(self, source, target, replace):
        ### 验证数据
        # 判断目录存在
        if not os.path.isdir(source):
            LogInfo.put (u'这个函数是用来传送本地目录的')
            return

        ### 处理数据
        # 遍历目录内容，上传资源
        for file in os.listdir(source):
            # 资源路径
            filepath = os.path.join(source, file)

            # 判断资源文件类型
            if os.path.isfile(filepath):
                # 1.文件
                self.uploadFile(filepath, file, replace)
            elif os.path.isdir(filepath):
                # 2.目录
                try:
                    self.sftp.chdir(file)
                except:
                    self.sftp.mkdir(file)
                    self.sftp.chdir(file)
                self.uploadDir(filepath, file, replace)

        ### 重置数据
        # 返回上一层目录
        self.sftp.chdir('..')

    # 传送文件
    def uploadFile(self, filepath, filename, replace):
        ### 验证数据
        # 验证文件类型
        if not os.path.isfile(filepath):
            LogInfo.put(u'这个函数是用来传送单个文件的')
            return
        # 验证文件存在
        if not os.path.exists(filepath):
            LogInfo.put (u'err:本地文件不存在，检查一下'+filepath)
            return
        # 验证FTP已连接
        if self.sftp == None:
            LogInfo.put (u'sftp 还未链接')
            return


        ### 处理数据
        # 判断文件存在是否覆盖
        if not replace:
            if filename in self.sftp.listdir():
                LogInfo.put (u'[*] 这个文件已经存在了，选择跳过:' + filepath + ' -> ' + self.sftp.getcwd() + '/' + filename)
                return
        # 上传文件
        try:
            self.sftp.put(filepath, filename)
            LogInfo.put (u'[+] 上传成功:' + filepath + ' -> ' + self.sftp.getcwd() + '/' + filename)
        except Exception as e:
            LogInfo.put (u'[+] 上传失败:' + filepath + ' because ' + str(e))


    # 获得文件媒体数据({文件/目录, 文件名称})
    def __filetype(self, source):
        # 判断文件类型
        if os.path.isfile(source):
            # 1.文件
            index = source.rfind('/')
            return _XFER_FILE, source[index+1:]
        elif os.path.isdir(source):
            # 2.目录
            return _XFER_DIR, ''


    # 创建目标路径
    # 说明: 目标路径不存在则依次创建路径目录
    def __makePath(self, target):
        # 切换根目录
        self.sftp.chdir('/')
        # 分割目标目录为目录单元集合
        data = target.split('/')
        # 进入目标目录, 目录不存在则创建
        for item in data:
            try:
                self.sftp.chdir(item)
                LogInfo.put (u'要上传的目录已经存在，选择性进入合并：' + item)
            except:
                try:
                    self.sftp.mkdir(item)
                    self.sftp.chdir(item)
                    LogInfo.put (u'要上传的目录不存在，创建目录：' + item)
                except Exception as e:
                    LogInfo.put('upload error:'+str(e.args))

    def download_file(self, local, remote):  # 下载当个文件
        try:
            # file_handler = open(local, 'wb')
            self.sftp.get(remote.replace('\\','/'), local.replace('\\','/')) # 下载目录中文件
            LogInfo.put(u'下载文件' + remote.replace('\\', '/')+'成功')
            # file_handler.close()
        except Exception as e:
            LogInfo.put(u'下载文件' + remote.replace('\\', '/')+'失败，'+str(repr(e)))

    def download_files(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)
        try:
            for file in self.sftp.listdir(RemoteDir):
                Local = os.path.join(LocalDir, file)
                Remote = os.path.join(RemoteDir, file)
                if file.find(".") == -1:  # 判断是否是文件
                    if not os.path.exists(Local):
                        os.makedirs(Local)
                    self.download_files(Local.replace('\\','/'), Remote.replace('\\','/'))
                else:  # 文件
                    self.download_file(Local.replace('\\','/'), Remote.replace('\\','/'))
        except:
            Local = os.path.join(LocalDir, RemoteDir.split('/')[-1])
            self.download_file(Local, RemoteDir)
        LogInfo.put('--download over--')

    def run(self,cmd):
        try:
            for m in cmd:
                stdin,stdout,stderr=self.sftp.exec_command(m)
                LogInfo.put(stderr.read())
                LogInfo.put(stdout.read())
                LogInfo.put("Check Status: %s\tOK\n"%(self.arg['ip']))
        except Exception as e:
            print(e)
            LogInfo.put("%s\tError\n"%(self.arg['ip']))





if __name__ == '__main__':
    arg = {'ip':'42.121.18.62','user':'yarlungroot','password':'ys2root4','port':22}
    me  = RemoteHelper(arg)
    me.startup()
    # 要上传的本地文件夹路径
    source = r'C:/Users/Shinelon/Desktop/cmd'
    # 上传到哪里 [远程目录]
    target = r'/home/yarlungroot/.mozilla'
    replace = False

    # me.upload(source, target, replace)
    # me.download_files(source, target)
    me.run(('free',))
    me.shutdown()