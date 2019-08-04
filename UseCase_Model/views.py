
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
os.environ['DJANGO_SETTINGS_MODULE'] ='InterFace_Test.settings'#使用django的model或model内部使用外部文件，必须定义这三句
import django
django.setup()
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from src.run_AllTest import AllTest
from src.utils.customize import Page,get_page_index
from UseCase_Model.models import RobotTestUseCase,TestReport
import json

num_progress = 0 #当前的后台进度值
# Create your views here.

'''测试用例页面相关操作'''
def exec_unittest(request):
    p = request.GET['page'] if request.GET.get('page') else 1
    ctx = {"page":{"page_index":p}}
    return render(request,'index.html',ctx)

#post
def go_unittest(request):
    print("进来了",request.body)
    ctx = {"msg":"执行失败"}
    if request.body:
        try:
            body_data = json.loads(request.body)
            test_text = body_data.get('test_name')
            print("进来了test_text",test_text)
            run_alltest = AllTest()
            msg = run_alltest.run()
            ctx['msg'] = '{},{}'.format(test_text,msg)
        except Exception as e:
            ctx['msg'] = '自动化执行失败，error:{}'.format(e)
    #return render(request,'index.html',ctx)
    return HttpResponse(json.dumps(ctx))

#返回进度值
def show_progress(request):
    print("进度值为：",num_progress)
    return JsonResponse(num_progress,safe=False)

#分页返回用例表内容:
def data_unittes(request):
    request.encoding = 'utf-8'
    #print("测试：：》",request.GET)
    page = request.GET['page'] if request.GET.get('page') else '1'
    #print("测试：：》page",page)
    page_index = get_page_index(page)
    num = RobotTestUseCase.objects.all().count()
    print("num为:%s page_index为:%s"%(str(num),str(page_index)))
    p = Page(num,page_index)
    pa = {
        "has_next":p.has_next,
        "has_previous":p.has_previous,
        "item_count":p.item_count,
        "limit":p.limit,
        "offset":p.offset,
        "page_count":p.page_count,
        "page_index":p.page_index,
        "page_size":p.page_size
    }
    result = {
        "page":pa,
        "usecaselist":[]
    }
    print(result["page"])
    if num != 0:
        #result['usecaselist'] = serializers.serialize("json",RobotTestUseCase.objects.all()[p.offset:p.limit])
        sql = "select * from usecase_model_robottestusecase limit %s offset %s"%(p.limit,p.offset)
        #re = RobotTestUseCase.objects.all()[p.offset:p.limit]
        re = RobotTestUseCase.objects.raw(sql)
        datalist=[]
        for var in re:
            datas={
                "id" : var.id,
                "utter" : var.utter,
                "nowtime" : var.nowtime,
                "session_id" : var.session_id,
                "expectResults" :var.expectResults
            }
            datalist.append(datas)
        #print(datalist)
        result['usecaselist'] = datalist
    print("第",str(page),"次请求结果：",result)
    return HttpResponse(json.dumps(result))
    #return render(request,'index.html',result)

'''测试报告页面相关操作'''
#跳转到测试报告列表
def go_report(request):
    p = request.GET['page'] if request.GET.get('page') else 1
    ctx = {"page":{"page_index":p}}
    return render(request,'report.html',ctx)

#返回测试报告列表：
def test_report(request):
    request.encoding = 'utf-8'
    page = request.GET['page'] if request.GET.get('page') else '1'
    page_index = get_page_index(page)
    num =  TestReport.objects.all().count()
    print("num为:%s page_index为:%s"%(str(num),str(page_index)))
    p = Page(num,page_index)
    pa = {
        "has_next":p.has_next,
        "has_previous":p.has_previous,
        "item_count":p.item_count,
        "limit":p.limit,
        "offset":p.offset,
        "page_count":p.page_count,
        "page_index":p.page_index,
        "page_size":p.page_size
    }
    result = {
        "page":pa,
        "testreport":[]
    }
    if num != 0:
        sql = "select * from usecase_model_testreport limit %s offset %s"%(p.limit,p.offset)
        #re = RobotTestUseCase.objects.all()[p.offset:p.limit]
        re = RobotTestUseCase.objects.raw(sql)
        datalist=[]
        for var in re:
            datas={
                "id" : var.id,
                "testreport" : var.testreport,
                "create_time" : str(var.create_time),
                "note" : var.note
            }
            datalist.append(datas)
        result['testreport'] = datalist
    return HttpResponse(json.dumps(result))

#显示测试报告网页内容：
def show_report(request):
    report_name = request.GET['report_name'] if request.GET.get('report_name') else 'report_blank.html'
    return render(request,report_name)
    

if __name__ == '__main__':
    # run_alltest = AllTest()
    # msg = run_alltest.run()
    # print(msg)
    num = RobotTestUseCase.objects.all().count()
    #re = RobotTestUseCase.objects.order_by("id")[1:11]
    sql = "select * from usecase_model_robottestusecase limit %s offset %s"%(10,10)
    re = RobotTestUseCase.objects.raw(sql)
    print(re.query)
    datalist=[]
    for var in re:
        datas={
                "id" : var.id,
                "utter" : var.utter,
                "nowtime" : var.nowtime,
                "session_id" : var.session_id,
                "expectResults" :var.expectResults
        }
        datalist.append(datas)
    print(datalist)
    p = Page(num,1)
    print(num)