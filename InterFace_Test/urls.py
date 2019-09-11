"""InterFace_Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from UseCase_Model import views

urlpatterns = [
    path('admin/', admin.site.urls),#django 管理页面
    path('index/',views.exec_unittest), #首页
    path('test/',views.go_unittest),#执行接口自动化测试
    re_path('index/data_unittes/',views.data_unittes),#显示测试用例表
    re_path('progress_monitor/',views.show_progress),#显示测试进度条
    re_path('index/add/',views.add_usecase),#新增测试用例
    re_path('index/edit/',views.edit_usecase),#修改测试用例
    re_path('index/del/',views.del_usecase),#删除测试用例
    path('go_report/',views.go_report),#测试报告列表页
    re_path('index/test_report/',views.test_report),#显示测试报告列表
    re_path('go_report/show_report/',views.show_report),#查看测试报告
    re_path('go_report/del/',views.del_report),#删除测试报告
]
