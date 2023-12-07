from django.contrib import admin
from .models import Article
from .models import Comment

# Register your models here.

admin.site.register(Article)  # 为模型进行admin界面的注册
admin.site.register(Comment)
