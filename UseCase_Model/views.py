
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
    #获取分页信息：
    page = request.GET['page'] if request.GET.get('page') else '1'
    page_index = get_page_index(page)
    num = RobotTestUseCase.objects.all().count()
    print("num为:%s page_index为:%s"%(str(num),str(page_index)))
    p = Page(num,page_index)

    # #页数列表
    # page_list = []
    # for i in range(int(p.page_count)):
    #     page_list.append(i+1)

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
    #print(result["page"])

    #获取数据库记录：
    if num != 0:
        #result['usecaselist'] = serializers.serialize("json",RobotTestUseCase.objects.all()[p.offset:p.limit])
        sql = "select * from usecase_model_robottestusecase limit %s offset %s"%(p.limit,p.offset)
        #re = RobotTestUseCase.objects.all()[p.offset:p.limit]
        re = RobotTestUseCase.objects.raw(sql)
        datalist=[]
        try:
            page_id = (int(page)-1)*int(pa["limit"]) #重新排序id，防止删除一条记录后id排序断层
        except:
            page_id = 0
        for var in re:
            page_id += 1
            datas={
                "page_id":page_id,
                "id" : var.id,
                "utter" : var.utter,
                "nowtime" : var.nowtime,
                "session_id" : var.session_id,
                "expectResults" :var.expectResults
            }
            datalist.append(datas)
        #print(datalist)
        result['usecaselist'] = datalist
    #print("第",str(page),"次请求结果：",result)
    return HttpResponse(json.dumps(result))
    #return render(request,'index.html',result)

#新增测试用例
def add_usecase(request):
    #print("进来啦")
    ctx = {"code":200,"status":""}
    try:
        from_data = json.loads(request.body)
        if from_data:
            utter = from_data.get("add_utter")
            nowtime = from_data.get("add_nowtime")
            session_id = from_data.get("add_session_id")
            expectResults = from_data.get("add_expectResults")
            print("新增内容：",utter,nowtime,session_id,expectResults)
            new_usecase = RobotTestUseCase(utter=utter,nowtime=nowtime,session_id=session_id,expectResults=expectResults)
            new_usecase.save()
            ctx["status"] = "success"
        else:
            ctx["status"] = "There is no use data"
    except Exception as e:
        print("添加失败：",e)
        ctx["status"] = "{}:{}".format("add failer",str(e))
    return HttpResponse(json.dumps(ctx))

#修改测试用例
def edit_usecase(request):
    #print("进来啦")
    ctx = {"code":200,"status":""}
    print(" request.body:",request.body)
    try:
        from_data = json.loads(request.body)
        if from_data:
            original_id = from_data.get("original_id")
            utter = from_data.get("new_utter")
            nowtime = from_data.get("new_nowtime")
            session_id = from_data.get("new_session_id")
            expectResults = from_data.get("new_expectResults")
            print("更新开始：",original_id,utter,nowtime,session_id,expectResults)
            usecase = RobotTestUseCase.objects.get(id=original_id)
            usecase.utter = utter
            usecase.nowtime = nowtime
            usecase.session_id = session_id
            usecase.expectResults = expectResults
            usecase.save()
            ctx["status"] = "success"
        else:
            ctx["status"] = "There is no use case"
    except Exception as e:
        print("更新失败：",e)
        ctx["status"] = "{}:{}".format("update failer",str(e))
    return HttpResponse(json.dumps(ctx))

#删除测试用例
def del_usecase(request):
    #print("黄思远进来啦")
    ctx = {"code":200,"status":""}
    try:
        original_id = request.GET['original_id'] if request.GET.get('original_id') else None
        #print("original_id",original_id)
        if original_id:
            usecase = RobotTestUseCase.objects.get(id=original_id)
            usecase.delete()
            ctx["status"] = "success"
        else:
            ctx["status"] = "can't load original_id"
    except Exception as e:
        ctx["status"] = "{}:{}".format("delete failer",str(e))
    return HttpResponse(json.dumps(ctx))



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
        try:
            page_id = (int(page)-1)*int(pa["limit"]) #重新排序
            #print("page_id",page_id)
        except:
            page_id = 0
        for var in re:
            page_id += 1
            datas={
                "id" : var.id,
                "page_id":page_id,
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

def del_report(request):
    ctx = {"code":200,"status":""}
    try:
        original_id = request.GET['id'] if request.GET.get('id') else None
        #print("original_id",original_id)
        if original_id:
            Report = TestReport.objects.get(id=original_id)
            Report.delete()
            Report_name = Report.testreport
            report_path = "./src/report"
            if (os.path.exists(os.path.join(report_path, Report_name))):
                os.remove(os.path.join(report_path, Report_name))
                ctx["status"] = "success"
                #print("删除成功",report_path,Report_name)
            else:
                ctx["status"] = "success,but the file can't find"
                #print("删除失败",report_path,Report_name)
        else:
            ctx["status"] = "can't load original_id"
    except Exception as e:
        ctx["status"] = "{}:{}".format("delete failer",str(e))
    return HttpResponse(json.dumps(ctx))

if __name__ == '__main__':
    # run_alltest = AllTest()
    # msg = run_alltest.run()
    # print(msg)
    # num = RobotTestUseCase.objects.all().count()
    # #re = RobotTestUseCase.objects.order_by("id")[1:11]
    # sql = "select * from usecase_model_robottestusecase limit %s offset %s"%(10,10)
    # re = RobotTestUseCase.objects.raw(sql)
    # print(re.query)
    # datalist=[]
    # for var in re:
    #     datas={
    #             "id" : var.id,
    #             "utter" : var.utter,
    #             "nowtime" : var.nowtime,
    #             "session_id" : var.session_id,
    #             "expectResults" :var.expectResults
    #     }
    #     datalist.append(datas)
    # print(datalist)
    # p = Page(num,1)
    # print(num)
    usecase = RobotTestUseCase.objects.get(id=1)
    usecase.utter = "黄大仙"
    usecase.nowtime = "	1111222"
    usecase.session_id = "561616"
    usecase.expectResults = "test"
    usecase.save()
    print("done!")
