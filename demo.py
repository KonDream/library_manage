import mysql.connector
import tkinter as tk

mydb = mysql.connector.connect(
    host="127.0.0.1",  # 数据库主机地址
    user="xxx",  # 数据库用户名
    passwd="xxx",  # 数据库密码
    database="books"  # 连接数据库
)

# 创建一个游标 方便对数据库的操作
mycursor = mydb.cursor()


# # 创建表
# mycursor.execute(
#     "CREATE TABLE books (id INTEGER, author_name VARCHAR(64), name VARCHAR(64), CONSTRAINT books_pk PRIMARY KEY(id))")
# 借阅表
# mycursor.execute(
#     "CREATE TABLE borrow_list (id INTEGER, author_name VARCHAR(64), name VARCHAR(64))")


# 插入数据
# sql = "INSERT INTO books (id, author_name, name) VALUES (%s, %s, %s)"
# val = [
#     ('1', '金庸', '射雕英雄传'),
#     ('2', '金庸', '天龙八部'),
#     ('3', '金庸', '鹿鼎记'),
#     ('4', '金庸', '笑傲江湖'),
#     ('5', '古龙', '武林外史'),
#     ('6', '古龙', '小李飞刀'),
#     ('7', '古龙', '萧十一郎'),
#     ('8', '鲁迅', '阿Q正传'),
#     ('9', '鲁迅', '狂人日记'),
#     ('10', '巴金', '家'),
#     ('11', '巴金', '春'),
#     ('12', '巴金', '秋')
# ]
#
# mycursor.executemany(sql, val)
#
# mydb.commit()  # 数据表内容有更新，必须使用到该语句

# print(mydb)


class database_op(object):
    def __init__(self):
        self.c1 = mycursor

    def select(self):
        self.c1.execute("select * from books")
        for self.x in self.c1:
            print(self.x)
        print("----------查询成功----------")

    def add(self):
        # 获取要插入的书的编号
        self.c1.execute("SELECT max(id) from books")
        self.a = self.c1.fetchone()
        for self.x in self.a:
            self.id = self.x + 1

        self.book_name = input("请输入书名: ")
        # 判断数据库里有没有这本书，如果有这本书了，就拒绝添加操作
        self.c1.execute("SELECT name FROM books WHERE name = '%s'" % self.book_name)
        if self.c1.fetchone() is not None:
            print("这本书已经入库，请返回重新查询~")
        else:  # 否则执行插入操作
            # 获取author表中书名的编号
            self.author_name = input("请输入作者名: ")
            # 查询
            self.sql = "INSERT INTO books (id, author_name, name) VALUES ('%s', '%s', '%s')" % (
                self.id, self.author_name, self.book_name)
            self.c1.execute(self.sql)
            print("添加成功！")
            mydb.commit()

    def delete(self):
        self.pwd = input("请输入超级vip专享密码：")
        if self.pwd == 'vip666':
            self.delete_vip()
        else:
            print("密码错误！")
            exit()

    def delete_vip(self):
        self.no = int(input("请输入要删除的图书序号或0以退出："))
        if self.no == 0:
            print("已退出删除")
            pass
        else:
            self.c1.execute("SELECT id FROM books WHERE id = '%d'" % self.no)
            # 判断是否存在将要删除的书
            if self.c1.fetchone() is None:
                self.flag = 1
                print("输入序号有误，请重新输入~")
                self.delete_vip()
            else:
                self.c1.execute("DELETE FROM books WHERE id = '%d'" % self.no)
                print("删除成功！")
                mydb.commit()

    def search(self):
        print("输入1查询某作者的所有图书")
        print("输入2查询某图书的作者")
        self.no = int(input("请输入查询（1,2）："))
        if self.no == 1:
            self.author_name = input("请输入作者名：")
            self.c1.execute("SELECT name FROM books WHERE author_name = '%s'" % self.author_name)
            self.a = self.c1.fetchall()
            # 判断当前列表是否为空
            if not self.a:
                print("暂无此作者的藏书！")
            else:
                print("%s的书：" % self.author_name)
                for self.x in self.a:
                    print(self.x[0])
        elif self.no == 2:
            self.book_name = input("请输入书名：")
            self.c1.execute("SELECT author_name FROM books WHERE name = '%s'" % self.book_name)
            self.a = self.c1.fetchone()
            if self.a is None:
                print("没有这本藏书！")
            else:
                print("%s的作者：" % self.book_name)
                for self.x in self.a:
                    print(self.x)
        else:
            print("输入有误，请重新输入：")
            self.search()

    def update(self):
        self.c1.execute("SELECT COUNT(*) from books")
        self.a = self.c1.fetchone()
        for self.x in self.a:
            self.allbooks_no = self.x
        self.book_no = int(input("请输入要更新的图书序号："))
        # 判断要更新的序号是否在库中
        if self.book_no > self.allbooks_no or self.book_no <= 0:
            print("输入有误，请重新输入：")
            self.update()
        else:
            print("输入1更新图书名")
            print("输入2更新作者名")
            self.no = int(input("请输入更新（1,2）："))
            if self.no == 1:
                self.new_book = input("请输入要更新的图书名：")
                self.c1.execute("UPDATE books SET name = '%s' WHERE id = '%d'" % (self.new_book, self.book_no))
                print("更新成功！")
                mydb.commit()
            elif self.no == 2:
                self.new_author = input("请输入要更新的作者名：")
                self.c1.execute("UPDATE books SET author_name = '%s' WHERE id = '%d'" % (self.new_author, self.book_no))
                print("更新成功！")
                mydb.commit()
            else:
                print("输入有误，请重新输入：")
                self.update()

    def borrow(self):
        self.no = int(input("请输入要借阅书的序号："))
        self.c1.execute("SELECT id FROM borrow_list WHERE id = '%s'" % self.no)
        if self.c1.fetchone() is not None:
            print("此书已经被借走！")
        else:
            self.c1.execute("SELECT max(id) from books")
            self.a = self.c1.fetchone()
            for self.x in self.a:
                self.allbooks_no = self.x
            self.c1.execute("SELECT id from books limit 1")
            for self.x in self.c1.fetchone():
                self.first_no = self.x
            if self.no > self.allbooks_no or self.no < self.first_no:
                print("输入有误，请重新输入：")
                self.borrow()
            else:
                self.c1.execute("SELECT author_name FROM books WHERE id = '%d'" % self.no)
                for self.x in self.c1.fetchone():
                    self.author_name = self.x
                self.c1.execute("SELECT name FROM books WHERE id = '%d'" % self.no)
                for self.x in self.c1.fetchone():
                    self.book_name = self.x
                self.c1.execute("DELETE FROM books WHERE id = '%d'" % self.no)
                self.c1.execute(
                    "INSERT INTO borrow_list (id, author_name, name) VALUES ('%d', '%s', '%s')" % (self.no, self.author_name,
                                                                                                   self.book_name))
                print("借阅成功！")
                mydb.commit()

    def select_borrow(self):
        self.c1.execute("select * from borrow_list")
        for self.x in self.c1:
            print(self.x)
        print("----------查询成功----------")

    def return_books(self):
        self.no = int(input("请输入要归还书的序号："))
        self.c1.execute("SELECT max(id) from borrow_list")
        self.a = self.c1.fetchone()
        for self.x in self.a:
            self.allbooks_no = self.x
        self.c1.execute("SELECT id from borrow_list limit 1")
        for self.x in self.c1.fetchone():
            self.first_no = self.x
        if self.no > self.allbooks_no or self.no < self.first_no:
            print("输入有误，请重新输入：")
            self.return_books()
        else:
            self.c1.execute("SELECT author_name FROM borrow_list WHERE id = '%d'" % self.no)
            for self.x in self.c1.fetchone():
                self.author_name = self.x
            self.c1.execute("SELECT name FROM borrow_list WHERE id = '%d'" % self.no)
            for self.x in self.c1.fetchone():
                self.book_name = self.x
            self.c1.execute("DELETE FROM borrow_list WHERE id = '%d'" % self.no)
            self.c1.execute(
                "INSERT INTO books (id, author_name, name) VALUES ('%d', '%s', '%s')" % (self.no, self.author_name,
                                                                                               self.book_name))
            print("归还成功！")
            mydb.commit()


if __name__ == '__main__':
    # w = windows(master=tk.Tk())
    # w.mainloop()
    db = database_op()
    print("----------欢迎进入klx的藏书阁----------")
    print("输入数字即可操作本藏书阁：")
    print("输入1 ：查询藏书阁中所有图书")
    print("输入2 ：为藏书阁添砖加瓦（添加新的书）")
    print("输入3 ：删除图书（超级vip可用）")
    print("输入4 ：查询某本图书")
    print("输入5 ：修正某本书")
    print("输入6 ：借阅某本书")
    print("输入7 ：查询借阅列表")
    print("输入8 ：归还某本书")
    print("输入886 ：离开藏书阁")
    print("----------欢迎进入klx的藏书阁----------")
    while True:
        no = input("请输入操作序号（1,2,3,4,5,6,7,8,886）：")
        if no == '1':
            db.select()
        elif no == '2':
            db.add()
        elif no == '3':
            db.delete()
        elif no == '4':
            db.search()
        elif no == '5':
            db.update()
        elif no == '6':
            db.borrow()
        elif no == '7':
            db.select_borrow()
        elif no == '8':
            db.return_books()
        elif no == '886':
            print("----------欢迎再次光临藏书阁----------")
            exit()
        else:
            print("输入有误，请重新输入~")
