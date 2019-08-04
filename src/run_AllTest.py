#-*- coding:utf-8 -*-
'''
filename : run_AllTest.py
create by : 
create time : 2019/07/09
introduce : 执行自动化接口测试总入口，具体操作包括：
            1、执行指定单元测试文件
            2、生成测试报告
            3、发送测试报告邮件通知
'''
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import unittest
import time
import src.HTMLTestRunner as HTMLTestRunner
from src.db_fixture import test_data
from src.utils.readConfig import readConfig
from src.utils.configEmail import sendemail
from src.db_fixture import data_operation
from src.utils.log import logger
from UseCase_Model import views

 
report_path = os.path.join(parentdir, 'src\\report\\')
on_off = readConfig.get_email('on_off')
 
class AllTest:#定义一个类AllTest
    def __init__(self):#初始化一些参数和数据

        now = time.strftime("%Y-%m-%d %H_%M_%S")
        self.fn = now + '_result.html'#定义自动化测试文件名
        self.caseListFile = os.path.join(parentdir, "src\\caselist.txt")#配置执行哪些测试文件的配置文件路径
        self.caseFile = os.path.join(parentdir, "src\\interface")#真正的测试断言文件路径
        self.caseList = []
 
    def set_case_list(self):
        """
        读取caselist.txt文件中的用例名称，并添加到caselist元素组
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):# 如果data非空且不以#开头
                self.caseList.append(data.replace("\n", ""))#读取每行数据会将换行转换为\n，去掉每行数据中的\n
        fb.close()
 
    def set_case_suite(self):
        """
        :return:
        """
        self.set_case_list()#通过set_case_list()拿到caselist元素组
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:#从caselist元素组中循环取出case
            case_name = case.split("/")[-1]#通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
            print(case_name+".py")#打印出取出来的名称
            #批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)#将discover存入suite_module元素组
            print('suite_module:'+str(suite_module))
        if len(suite_module) > 0:#判断suite_module元素组是否存在元素
            for suite in suite_module:#如果存在，循环取出元素组内容，命名为suite
                for test_name in suite:#从discover中取出test_name，使用addTest添加到测试集
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        return test_suite#返回测试集
 
    def run(self):
        """
        run test
        :return:
        """
        start_time = time.time()
        msg = ''
        try:
            logger.info("自动化测试开始......")
            print("自动化测试开始......")
            #test_data.init_data() # 初始化接口测试数据
            suit = self.set_case_suite()#调用set_case_suite获取test_suite

            if suit is not None:#判断test_suite是否为空

                filename = report_path + self.fn
                fp = open(filename, 'wb')#打开result/20181108/report.html测试报告文件，如果不存在就创建
                #调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description:')
                runner.run(suit)
                msg = '自动化接口测试执行成功！'
                data_operation.insert_report(self.fn,msg)
            else:
                logger.info("Have no case to test.")
                msg = '没有可执行测试集！'
        except Exception as ex:
            logger.info("test error:",str(ex))
            print("test error:",str(ex))
            msg = '{}:{}'.format('自动化接口测试执行失败：',str(ex))
 
        finally:
            logger.info("自动化测试结束......")
            print("自动化测试结束......")
            fp.close()

        end_time = time.time()
        exec_time = (end_time - start_time)*1000
        logger.info(f"耗时{exec_time}ms")
        #判断邮件发送的开关
        logger.info("发送测试报告......")
        print("发送测试报告......")
        if on_off == 'on':
            sendemail.send(self.fn)
            logger.info("测试报告发送成功，请打开邮箱查看......")
            print("测试报告发送成功，请打开邮箱查看......")
        else:
            logger.info("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")
            print("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")
        logger.info("=="*20)
        return msg

 
if __name__ == '__main__':
    AllTest().run()
    a = views.num_progress
    print(a)