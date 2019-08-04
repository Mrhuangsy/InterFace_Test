#-*- coding:utf-8 -*-
'''
filename : test_data.py
create by : 
create time : 2019/07/09
introduce : 编写测试用例，并保存到指定数据库表
'''
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import uuid
from db_fixture.mysql_db import DB
 
# create data
datas = {
  'myusecase':[
    { 'utter':'你是谁',
      'NowTime':'111125422',
      'session_id':str(uuid.uuid1()),
      'expectResults':'“test'
      },
    {'utter': '在干嘛',
     'NowTime': '111125423',
     'session_id': str(uuid.uuid1()),
     'expectResults': '“test'
     },
    {'utter': '天气好冷哦',
     'NowTime': '111125424',
     'session_id': str(uuid.uuid1()),
     'expectResults': '“test'
     }
  ]
}
 
# Inster table datas
def init_data():
  DB().init_data(datas)
 
 
if __name__ == '__main__':
  init_data()