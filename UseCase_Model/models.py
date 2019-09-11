from django.db import models

# Create your models here.
class RobotTestUseCase(models.Model):
    #测试用例表
    utter = models.CharField(max_length=60)
    nowtime = models.CharField(max_length=20)
    session_id = models.CharField(max_length=20)
    expectResults = models.CharField(max_length=60)

    def __str__(self):
        return self.utter,self.nowtime,self.session_id,self.expectResults
    

class TestReport(models.Model):
    #测试报告
    testreport = models.CharField(max_length=60)
    create_time = models.DateTimeField()
    note = models.CharField(max_length=60)