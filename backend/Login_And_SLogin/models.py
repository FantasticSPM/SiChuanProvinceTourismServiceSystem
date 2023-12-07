# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


# class UserManager(models.Manager):
#     def get_by_natural_key(self, username):
#         return self.get(username=username)


class UserTable(AbstractUser):  # 建立用户数据模型
    age = models.IntegerField(null=True, blank=True)  # 用户年龄 blank设置为True，可以不填，默认使用none填充数据库
    sex = models.CharField(max_length=2, null=True, blank=True)  # 用户性别

    # objects = UserManager()

    def natural_key(self):  # 引入自然键帮助更好的显示数据
        return (self.username)
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["username"],
    #             name="the_username",
    #         ),
    #     ]
