import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0,parentdir)
os.environ['DJANGO_SETTINGS_MODULE'] ='InterFace_Test.settings'#使用django的model必须定义这三句
import django
django.setup()
import datetime
from UseCase_Model.models import TestReport #导入数据表模型

def insert_report(report_name,note):
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #获取当前时间
    test_report_list = TestReport(testreport = report_name,create_time = nowtime,note=note)
    test_report_list.save()