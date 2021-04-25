import sqlite3
import time

class SqlController:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.curs = self.conn.cursor()

    def create_DB(self):
        sql = "create table user" \
              "(" \
              "owner INTEGER PRIMARY KEY," \
              "username varchar(20)," \
              "password varchar(100)" \
              ")"
        self.curs.execute(sql)

        sql = "create table clock" \
              "(" \
              "owner int," \
              "time int," \
              "prescription varchar(255)," \
              "id int" \
              ")"
        self.curs.execute(sql)

        sql = "create table auto_update" \
              "(" \
              "owner INTEGER PRIMARY KEY"\
              ")"
        self.curs.execute(sql)

        self.conn.commit()

    def delete_DB(self):
        sql = "drop table user"
        self.curs.execute(sql)

        sql = "drop table clock"
        self.curs.execute(sql)

        sql = "drop table auto_update"
        self.curs.execute(sql)

        self.conn.commit()

    def write_user(self, number, username, password):
        sql = "replace into user values(%d,'%s','%s')" % (number, username, password)
        self.curs.execute(sql)

        self.conn.commit()

    def read_user(self, owner):
        sql = "select * from user where owner=%d" % owner
        cursor = self.curs.execute(sql)

        return cursor.fetchone()

    def write_clock(self, number, time, prescription, id):
        sql = "select * from clock where owner=%d and id=%d"%(number,id)
        if not self.curs.execute(sql).fetchall():
            sql = "insert into clock values({0},{1},'{2}',{3})".format(number, time, prescription, id)
            self.curs.execute(sql)

            self.conn.commit()

    def read_clock_by_time(self, time):
        sql = "select * from clock where time >= %d AND time <= %d" % (time*1000, time*1000+20*24*60*60*1000)
        cursor = self.curs.execute(sql)

        return cursor.fetchall()

    def read_clock_by_owner(self, owner):
        sql = "select * from clock where owner = %d" % owner
        cursor = self.curs.execute(sql)

        return cursor.fetchall()

    def delete_useless_clock(self):
        sql = "delete from clock where time < %d" %(time.time()*1000)
        self.curs.execute(sql)

        self.conn.commit()

    def add_auto_update(self, owner):
        sql = "replace into auto_update values(%d)" % owner
        self.curs.execute(sql)

        self.conn.commit()

    def delete_auto_update(self, owner):
        sql = "delete from auto_update where owner=%d"%owner
        self.curs.execute(sql)

        self.conn.commit()

    def get_auto_update(self):
        sql = "select * from auto_update"
        return self.curs.execute(sql).fetchall()

DDL_DB = SqlController("ddl.db")
