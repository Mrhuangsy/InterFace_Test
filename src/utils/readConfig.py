#-*- coding:utf-8 -*-
'''
filename : readConfig.py
create by : 
create time : 2019/07/09
introduce : 自定义方法，读取配置文件config.ini指定内容
'''
import os
import configparser

path = str(os.path.dirname(os.path.dirname(__file__)))
#path = base_dir.replace('\\', '/')
config_path = os.path.join(path, 'config.ini')#这句话是在path路径下再加一级，最后变成C:\Users\songlihui\PycharmProjects\dkxinterfaceTest\config.ini
config = configparser.ConfigParser()#调用外部的读取配置文件的方法
config.read(config_path, encoding='utf-8')
 
class ReadConfig():
 
    def get_http(self, name):#整形接口配置
        value = config.get('HTTP', name)
        return value
    def get_email(self, name):#邮箱配置
        value = config.get('EMAIL', name)
        return value
    def get_mysql(self, name):#数据库配置
        value = config.get('mysqlconf', name)
        return value
 

readConfig = ReadConfig()
if __name__ == '__main__':#测试一下，我们读取配置文件的方法是否可用
    print('HTTP中的baseurl值为：', ReadConfig().get_http('baseurl'))
    print('EMAIL中的开关on_off值为：', ReadConfig().get_email('on_off'))
