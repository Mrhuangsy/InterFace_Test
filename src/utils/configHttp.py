#-*- coding:utf-8 -*-
'''
filename : configHttp.py
create by : 
create time : 2019/07/09
introduce : 自定义接口请求方法
'''
import requests
import json
 
class RunMain():
 
    def send_post(self, url, data):# 定义一个方法，传入需要的参数url和data
        # 参数必须按照url、data顺序传入
        result = requests.post(url=url, data=data).json()# 因为这里要封装post方法，所以这里的url和data值不能写死
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res
 
    def send_get(self, url, data):
        '''原get方法'''
        result = requests.get(url=url, data=data)
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res
    
    def send_get2(self, url, data=None):
        '''自定义get方法'''
        result = requests.get(url=url, data=data)
        res = result.json()
        return res
 
    def run_main(self, method, url=None, data=None):#定义一个run_main函数，通过传过来的method来进行不同的get或post请求
        result = None
        if method == 'post':
            result = self.send_post(url, data)
        elif method == 'get':
            result = self.send_get2(url, data)
        else:
            print("method值错误！！！")
        return result
runmain = RunMain()
if __name__ == '__main__':#通过写死参数，来验证我们写的请求是否正确
    result = RunMain().run_main('get', 'http://192.168.1.18:8001/dialog_manager/v1/marketing_robot?client_utterance=丰胸&active=True&no_user_response=False&enterprise_id=171686&session_id=a20515e8-a13a-11e9-89e9-e0d55e7e3d0c&rid=a2053cda-a13a-11e9-bcb7-e0d55e7e3d0c&uid=test', None)
    print(result)
