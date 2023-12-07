# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from Login_And_SLogin.models import UserTable
from article.models import Article  # 导入Article模型
from article.models import Comment  # 导入Comment模型
import json
from django.http import HttpResponseBadRequest
# from django.utils import timezone
from django.core import serializers
import os
from backend import settings
import time


def index(request):  # 文章首页函数
    data = {}
    context = serializers.serialize(
        "json",
        [*Article.objects.all(), *Comment.objects.all()],  # 将文章和评论从数据库中读取
        use_natural_foreign_keys=True,  
        use_natural_primary_keys=True,  # 这两行保证django模型使用自然键
    )
    data["data"] = json.loads(context)
    return JsonResponse(data, safe=False)


def comment_control(request):  # 提交评论的处理函数
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(['False', '无效的数据'])
        comment_content = data.get('comment_content')
        article_id = data.get('article_id')
        pid = data.get('pid')
        usename = data.get('username')  # 获取当前用户的ID
        author = UserTable.objects.get(username=usename)
        Comment.objects.create(comment_content=comment_content,
                               pre_comment_id=pid,
                               article_id=article_id,
                               comment_author=author)  # 将提交的评论数据保存到数据库中
        return redirect("/article/index/")


def article_create(request):
    if request.method == 'POST':
        new_article_content = request.POST.get('content')
        usename = request.POST.get('usename')
        imgfile = request.FILES.get('img')
        if imgfile is not None:  # 实现上传图片功能
            init_time = str(time.time())
            imgfileurl = os.path.join(settings.IMAGE_ROOT, init_time + imgfile.name)
            with open(imgfileurl, 'wb') as f:
                for imgFile_Part in imgfile.chunks():
                    f.write(imgFile_Part)
            new_img_url = init_time + imgfile.name
        else:
            new_img_url = None
        new_article_username = UserTable.objects.get(username=usename)
        Article.objects.create(  # 向数据库中提交文章数据
            content=new_article_content,
            #    title=new_article_title,
            author=new_article_username,
            img_url=new_img_url)
        return redirect("/article/index/")


def article_delete(request):
    # 根据 id 获取需要删除的文章
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(['False', '无效的数据'])
    article_id = data.get('article_id')
    print(article_id)
    article = Article.objects.get(id=article_id)
    # 调用.delete()方法删除文章
    article.delete()
    return redirect("/article/index/")


def comment_delete(request):  # 根据 id 获取数据库中需要删除的文章并将其删除
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(['False', '无效的数据'])
    Comment_id = data.get('Comment_id')
    print(Comment_id)
    comment = Comment.objects.get(id=Comment_id)
    comment.delete()  # 调用.delete()方法删除文章
    return redirect("/article/index/")


