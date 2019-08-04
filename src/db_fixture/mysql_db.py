#-*- coding:utf-8 -*-
'''
filename : mysql_db.py
create by : 
create time : 2019/07/09
introduce : mysql数据库相关操作，包括删除、插入和查找
'''
import pymysql.cursors
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from utils.readConfig import readConfig as cf

# ======== Reading db_config.ini setting ===========
host = cf.get_mysql("host")
port = cf.get_mysql("port")
db  = cf.get_mysql("db_name")
user = cf.get_mysql("user")
password = cf.get_mysql("password")
# ======== MySql base operating ===================

class DB:
 
  def __init__(self):
    try:
      # Connect to the database
      self.connection = pymysql.connect(host=host,
                       port=int(port),
                       user=user,
                       password=password,
                       db=db,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
    except pymysql.err.OperationalError as e:
      print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
 
  # clear table data
  def clear(self, table_name):
    # real_sql = "truncate table " + table_name + ";"
    real_sql = "delete from " + table_name + ";"
    with self.connection.cursor() as cursor:
      cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
      cursor.execute(real_sql)
    self.connection.commit()
  
  # select sql statement
  def select(self,table_name,table_data={},column="*"):
    '''
    Args:
        -- table_name : string ,表名
        -- table_data : dict ,条件
        -- column : string,列名
    '''
    try:
      real_sql = f"SELECT {column} FROM {table_name} WHERE 1=1"
      conditions = ""
      for key,value in table_data.items():
          conditions += f" AND {key} = {value} "
      real_sql += conditions
      print("查询语句：",real_sql)
      
      with self.connection.cursor() as cursor:
        cursor.execute(real_sql)
        return cursor.fetchall()
    except Exception as e :
      print("查询失败：",e)
 
  # insert sql statement
  def insert(self, table_name, table_data):
    for key in table_data:
      table_data[key] = "'"+str(table_data[key])+"'"
    key  = ','.join(table_data.keys())
    value = ','.join(table_data.values())
    real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
    #print(real_sql)
 
    with self.connection.cursor() as cursor:
      cursor.execute(real_sql)
 
    self.connection.commit()
 
  # close database
  def close(self):
    self.connection.close()
 
  # init data
  def init_data(self, datas):
    for table, data in datas.items():
      self.clear(table)
      for d in data:
        self.insert(table, d)
    self.close()
 
 
if __name__ == '__main__':
 
  db = DB()
  table_name = "myusecase"
  # data = {'parameter1':'test','parameter2':'test','`parameter3`':'test','parameter4':'test'}
  # db.clear(table_name)
  # db.insert(table_name, data)
  # db.close()
  table_data = {"enterprise_id":"171686"}
  value = db.select(table_name)
  print(len(value))
  for i in range(len(value)):
    print(f"第{i}笔：")
    for key ,values in value[i].items():
          print(key,"-",values)
  db.close()