#-*- coding:utf-8 -*-
'''
filename : batch_dialog_manager_test.py
create by : 
create time : 2019/07/09
introduce : 单元测试文件
'''
import unittest
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0,parentdir)
os.environ['DJANGO_SETTINGS_MODULE'] ='InterFace_Test.settings'#使用django的model必须定义这三句
import django
django.setup()
from src.utils.readConfig import readConfig as cf #配置文件读取
from src.utils.configHttp import runmain as rq #接口请求
from UseCase_Model.models import RobotTestUseCase #导入数据表模型
from UseCase_Model import views

class BatchDialogueTest(unittest.TestCase):
    '''批量测试机器人对话'''
    def setUp(self):
        print("对话测试开始前准备")
        self.base_url = cf.get_http("roboturl")
        self.result = {}
    
    def tearDown(self):
        print("测试结束，输出log完结\n\n")

    def action(self,payload,expectResults):
        '''测试闲聊机器人对话管理接口'''
        views.num_progress = (views.num_progress+1)*10 #进度控制
        payload = payload.rstrip("&")
        url = self.base_url + payload
        self.result = rq.run_main("get",url)
        realResults = self.result['data'] if self.result.get('data') else ''
        self.assertEqual(self.result['code'],200)
        self.assertIsInstance(self.result['data'],str)
        self.assertEqual(realResults,expectResults)

    @staticmethod
    def getTestFunc(payload,expectResults):
        def func(self):
            self.action(payload,expectResults)
        return func

def __generateTestCases():
    #找出用例表中所有的用例
    usecase = RobotTestUseCase.objects.all()
    print("usecase:>",len(usecase))
    arglists = []
    for var in usecase:
        utter = var.utter
        nowtime = var.nowtime
        session_id = var.session_id
        expectResults = var.expectResults
        payload = f"?utter={utter}&nowtime={nowtime}&session_id={session_id}"
        arglists.append((payload,expectResults))
    #print(arglists)
    #i = 1
    for args in arglists:
        #views.num_progress = i * 100 /len(arglists) #进度控制
        setattr(BatchDialogueTest,'test_func_%s_%s'%(args[0],args[1]),
                BatchDialogueTest.getTestFunc(*args))
        #i += 1
    
__generateTestCases()

if __name__ == '__main__':
    unittest.main()
    print(views.num_progress)