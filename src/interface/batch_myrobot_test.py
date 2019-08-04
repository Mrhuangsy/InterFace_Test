#-*- coding:utf-8 -*-
'''
filename : batch_myrobot_test.py
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

class BatchDialogManagerTest(unittest.TestCase):
    '''测试对话管理'''
    def setUp(self):
        #self.db = DB()
        #http://39.96.87.250:8000/xiaohuang/@utter=<utter>&@NowTime=<NowTime>&@session_id=<session_id>
        self.base_url = "http://39.96.87.250:8000/xiaohuang/"

    def action(self,payload,expectResults):
        '''测试小黄'''
        payload = payload.rstrip("&")
        url = self.base_url + payload
        r = requests.get(url)
        self.result = r.json()
        realResults = self.result['data'] if self.result.get('data') else ''
        print(realResults)
        self.assertEqual(self.result['code'],200)
        self.assertIsInstance(self.result['data'],str)
        #self.assertEqual(realResults,expectResults)

    @staticmethod
    def getTestFunc(payload,expectResults):
        def func(self):
            self.action(payload,expectResults)
        return func

def __generateTestCases():
    arglists = [('@utter=你是谁&@NowTime=111125422&@session_id=46516555','test'),('@utter=在干嘛&@NowTime=111125423&@session_id=46516555','test'),('@utter=天气好冷哦&@NowTime=111125424&@session_id=46516555','test')]
    for args in arglists:
        setattr(BatchDialogManagerTest,'test_func_%s_%s'%(args[0],args[1]),
                BatchDialogManagerTest.getTestFunc(*args))
__generateTestCases()

if __name__ == '__main__':
    unittest.main()