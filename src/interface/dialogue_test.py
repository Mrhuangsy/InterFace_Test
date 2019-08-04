#-*- coding:utf-8 -*-
'''
filename : dialog_manager_test.py
create by : 
create time : 2019/07/09
introduce : 单元测试文件
'''
import unittest
import requests
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from db_fixture import test_data
from db_fixture.mysql_db import DB

class DialogueTest(unittest.TestCase):
    '''测试对话管理'''

    def setUp(self):
        self.db = DB()
        self.base_url = "http://39.96.87.250:8000/xiaohuang/"
        self.table_name = "myusecase"
        self.usecase = self.db.select(self.table_name)
        self.result = {}

    def tearDown(self):
        self.db.close()
        print(self.result)

    def test_beauty_dialog(self):
        '''测试闲聊机器人对话'''
        pass

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()