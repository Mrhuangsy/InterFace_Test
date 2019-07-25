from django.db import models

# Create your models here.
class RobotTestUseCase(models.Model):
    #测试用例表
    utter = models.CharField(max_length=60)
    nowtime = models.CharField(max_length=20)
    session_id = models.CharField(max_length=20)