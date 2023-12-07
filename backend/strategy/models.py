from django.db import models


# Create your models here.
class Strategy(models.Model):  # 建立攻略模型
    pname = models.CharField(max_length=50, verbose_name='地名')
    location = models.CharField(max_length=100, verbose_name='位置')
    level = models.CharField(max_length=2, verbose_name='等级')
    content = models.TextField(verbose_name='介绍内容')
    img_url = models.CharField(max_length=100, verbose_name='图片路径', blank=True)

    class Meta:
        db_table = 'strategy_tb'
        verbose_name = "攻略"
        verbose_name_plural = verbose_name
