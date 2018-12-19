import sqlite3


def resource_path(relative):
    import sys, os
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath('.'),relative)

class SQLHelper:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')

    def get_cursor(self):
        if self.conn:
            return self.conn.cursor()
        self.conn = sqlite3.connect('data.db')
        return self.conn.cursor()

    def creat_cmd_table(self):
        cu = self.get_cursor()
        cu.execute('SELECT count(*) FROM sqlite_master WHERE type = "table" AND name= "cmdx"')
        r = cu.fetchall()
        if len(r) > 0 and r[0][0] == 1:
            self.close(self.conn, cu)
            return
        cu.execute('create table cmdx (name varchar(100) primary key,cmd varchar(100),type varchar(50), dex int)')
        self.conn.commit()
        print('创建数据库表[cmdx]成功!')
        self.close(self.conn, cu)

    def creat_cmd_tab_table(self):
        cu = self.get_cursor()
        cu.execute('SELECT count(*) FROM sqlite_master WHERE type = "table" AND name= "cmdtab"')
        r = cu.fetchall()
        if len(r) > 0 and r[0][0] == 1:
            self.close(self.conn, cu)
            return
        cu.execute('create table cmdtab (name varchar(100) primary key, priority int)')
        self.conn.commit()
        print('创建数据库表[cmdtab]成功!')
        self.close(self.conn, cu)

    def creat_server_table(self):
        cu = self.get_cursor()
        cu.execute('SELECT count(*) FROM sqlite_master WHERE type = "table" AND name= "serverx"')
        r = cu.fetchall()
        if len(r) > 0 and r[0][0] ==1:
            self.close(self.conn, cu)
            return
        cu.execute('create table serverx (name varchar(100) primary key,ip varchar(50),  account varchar(50),pwd varchar(300),port int)')
        self.conn.commit()
        print('创建数据库表[serverx]成功!')
        self.close(self.conn, cu)

    def add_cmd_value(self, name, cmd, type, index):
        sql = 'insert into cmdx(name,cmd,type,dex) values("'+name+'","'+cmd+'","'+  type+'",'+str(index)+')'
        print(sql)
        cu = self.get_cursor()
        cu.execute(sql)
        self.conn.commit()
        self.close(self.conn, cu)

    def add_cmdtab_value(self, name, priority):
        sql = 'insert into cmdtab(name, priority) values("'+name+'",'+str(priority)+')'
        print(sql)
        cu = self.get_cursor()
        cu.execute(sql)
        self.conn.commit()
        self.close(self.conn, cu)


    def add_server_value(self, name, ip, account, pwd, port):
        sql = 'insert into serverx(name, ip, account, pwd, port) values ("'+name+'","'+ip+'","'+account+'","'+pwd+'",'+str(port)+')'
        print(sql)
        cu = self.get_cursor()
        cu.execute(sql)
        self.conn.commit()
        self.close(self.conn, cu)

    def query_cmds_value(self, type):
        sql = 'select name from cmdx where type = "'+type+'"'+'or type = "all11a" order by dex asc'
        cu = self.get_cursor()
        cu.execute(sql)
        r = cu.fetchall()
        names = []
        if len(r) > 0:
            for e in range(len(r)):
                names.append(r[e][0])
        return names

    def query_cmdtabs_value(self):
        sql = 'select name from cmdtab order by priority asc'
        cu = self.get_cursor()
        cu.execute(sql)
        r = cu.fetchall()
        names = []
        if len(r) > 0:
            for e in range(len(r)):
                names.append(r[e][0])
        return names

    def query_cmd_value(self, name):
        sql = 'select cmd from cmdx where name ="'+name+'"'
        cu = self.get_cursor()
        cu.execute(sql)
        r = cu.fetchall()
        if len(r) > 0:
            return r[0][0]
        return None

    def query_servers_value(self):
        sql = 'select * from serverx'
        cu = self.get_cursor()
        cu.execute(sql)
        r = cu.fetchall()
        ips = []
        if len(r) > 0:
            for e in range(len(r)):
                ips.append(r[e][0])
        return ips

    def query_server_value(self, name):
        sql = 'select * from serverx where name ="'+name+'"'
        cu = self.get_cursor()
        cu.execute(sql)
        r = cu.fetchall()
        if len(r) > 0:
               return r[0]
        return None

    def delete_cmd_value(self, name):
        sql = 'delete from cmdx where name ="'+name+'"'
        cu = self.get_cursor()
        cu.execute(sql)
        self.conn.commit()
        self.close(self.conn, cu)

    def update_cmd_value(self, index, name):
        sql = 'update cmdx set index =' + str(index) +'where name = "'+name+'"'
        cu = self.get_cursor()
        cu.execute(sql)
        self.conn.commit()
        self.close(self.conn, cu)

    def close(self, conn, cu):
        try:
            if cu is not None:
                cu.close()
        finally:
            if conn is not None:
              pass

if __name__ == '__main__':
   s =  SQLHelper()
   s.creat_cmd_table()
   print('add')
   s.add_cmd_value('free','xx',1)
   # s.add_cmd_value('cmd2', 'xx', 22)
   # s.add_cmd_value('cmd3', 'xx', 3)
   # print('query')
   print(s.query_cmd_value())
   # print('de2')
   # s.delete_cmd_value('xx2')
   # print('query')
   # s.query_cmd_value()
   # print('de1')
   # s.delete_cmd_value('xx1')
   # print('query')
   # s.query_cmd_value()
