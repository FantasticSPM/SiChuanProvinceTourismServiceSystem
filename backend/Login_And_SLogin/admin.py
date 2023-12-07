from django.contrib import admin
from .models import UserTable
# Register your models here.

admin.site.register(UserTable)  # 为模型进行admin界面的注册
