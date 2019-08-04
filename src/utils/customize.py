
#-*- coding:utf-8 -*-
'''
filename : customize.py
create by : 
create time : 2019/07/28
introduce : 一些定制类和方法
'''

#定义一个Page类用于存储分页信息
class Page(object):

    def __init__(self, item_count,page_index=1,page_size=10):
        '''
        item_count:总条数
        page_index:总页数
        page_size:每页的条数
        '''
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size >0 else 0)
        if (item_count == 0) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size*(page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count #下一页
        self.has_previous = self.page_index > 1 #前一页
        super(Page,self).__init__()
    
    def __new__(cls,*args,**kwargs):
        print('new %s'%cls)
        return super(Page,cls).__new__(cls)
    # def __str__(self):
    #     #把page类实例变成str
    #     return 'item_count:%s,page_count:%s,page_index:%s,page_size:%s,offset:%s,limit:%s'%\
    #         (self.item_count,self.page_count,self.page_index,self.page_size,self.offset,self.limit)
    
    # __repr__ = __str__

def get_page_index(page_str):
    '''将传入的字符串类型数字转为int'''
    p = 1
    try:
        p = int(page_str)
    except Exception as e:
        pass
    if p < 1:
        p = 1
    return p

if __name__ == "__main__":
   test = Page(24,1)
   print(test)