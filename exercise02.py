import pymysql


# 将数据库操作封装为类
class DB_Controller:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 password='1030',
                 database='stu',
                 charset='utf8', table='user'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.table = table
        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database,
                                  charset=self.charset)
        self.cur = self.db.cursor()

    # 注册方法
    def __register(self):
        print('注册账户')
        user_name, passwd = self.__input_info()
        sql = "insert into %s (user_name, passwd) values ('%s', '%s');" % (self.table, user_name, passwd)
        if not user_name:
            print('谢谢使用')
            return
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print('Failed:', e)
        else:
            print('注册成功')
        pass

    # 登录方法
    def __login(self):
        print('登录账户')
        while True:
            user_name, passwd = self.__input_info()
            sql = "select * from %s where user_name = '%s';" % (self.table, user_name)
            if not user_name:
                print('谢谢使用')
                return
            self.cur.execute(sql)
            info = self.cur.fetchone()
            if info is None:
                print('该用户不存在，登陆失败')
                continue
            if passwd == info[2]:
                print('登录成功')
                break
            else:
                print('密码错误，登陆失败，请重新输入密码')
        pass

    @staticmethod
    def __input_info():
        user_name = input("User name is:")
        passwd = input('Password is:')
        return user_name, passwd

    @staticmethod
    def __view():
        print('====================')
        print('======register======')
        print('=======login========')
        print('========quit========')
        print('====================')

    def close(self):
        self.cur.close()
        self.db.close()

    def main(self):
        while True:
            self.__view()
            cmd = input('Cmd:')
            if cmd == 'register':
                controller.__register()
            elif cmd == 'login':
                controller.__login()
            elif cmd == 'quit':
                print('退出系统，谢谢使用')
                break
            else:
                print('输入有误，请重新输入')
                continue
        self.close()


if __name__ == '__main__':
    controller = DB_Controller()
    controller.main()

