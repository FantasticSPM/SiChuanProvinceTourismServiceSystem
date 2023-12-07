from django.urls import path
from article import views  # 导入myapp中的视图函数

app_name = 'article'

urlpatterns = [
    path('index/', views.index),  # 文章首页路由
    path('comment_control/', views.comment_control),  # 提交评论处理的路由
    path('article_create/', views.article_create),  # 文章创建路由
    path('article_delete/', views.article_delete),  # 文章删除路由
    path('comment_delete/', views.comment_delete),  # 评论删除路由
]
