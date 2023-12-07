from django.urls import path

from . import views

app_name = 'strategy'

urlpatterns = [
    path("index/", views.index, name="index"),  # 攻略模块主要路由
    path('liuliang/', views.liuliang, name='liuliang'),  # 客流量查询路由
    path('monitor/', views.monitor, name='monitor'),  # 客源数据监控路由
]
