# Create your views here.
import json
from django.contrib import auth  # 认证系统
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.core import serializers
from .models import UserTable  # 用户信息存储数据库


def Login_Slogin(request):
    return render(request, 'userlogin.html')


# 使用auth（自带的用户认证系统）实现登录与注册功能
def auth_Register(request):
    """
    用户注册
    :param request: 用户请求信息
    :return: JSON数据
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as err:
            state = 3000
            information = '无效数据！请检查前端传递的JSON数据是否按照标准JSON格式正确传入:\n' + str(err)
            response_json = {"state": state,
                             "info": information,
                             "responseTime": timezone.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')
                             }
            return JsonResponse(response_json)
        user_name = data.get('username')  # 获取username的值
        user_password = data.get('password')  # 获取password的值，以下get雷同
        user_xb = data.get('user_xb')

        try:
            # 获取年龄
            user_age = int(data.get('user_age', '0'))
            # 获取性别
            if user_xb == '男' or user_xb == 0:  # 接受两种传入值的方法：1.0/1: 男/女;2.直接传入字符串男/女
                user_xb = '男'
            else:
                user_xb = '女'
        except ValueError as err:
            state = 1001
            information = '传入的数据出错：\n' + str(err)
            response_json = {"state": state,
                             "info": information,
                             "responseTime": timezone.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')
                             }
            return JsonResponse(response_json)

        if not user_name:
            state = 1001  # 状态码反馈信息，2***代表成功，1***代表传入数据发生错误。具体错误码与原因请查看API说明文档，同时“info”也将说明错误原因
            information = '用户名不能为空'  # 记录反馈详细信息，若程序未出现错误，则为OK；若出错，则记录错误详细信息，类似于控制台报错信息。
        else:
            try:
                UserTable.objects.create_user(username=user_name, age=user_age, password=user_password, sex=user_xb)
            except Exception as err:
                state = 3001
                information = err
            else:
                state = 2001  # 状态码0000代表并无错误出现，用户注册成功
                information = 'OK'  # 程序执行后反馈信息。“OK”表示程序正常运行，并且没有错误发生，用户正常注册成功！
        response_json = {"state": state,
                         "info": str(information),
                         "requestGet": {
                             "name": user_name,
                             "password": "invisible",
                             "age": user_age,
                             "sex": user_xb
                             },
                         "responseTime": timezone.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')
                         }
        return JsonResponse(response_json)
    else:
        state = 4004
        information = '请求方式错误"GET"'
        response_json = {"state": state,
                         "info": str(information),
                         "responseTime": timezone.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')
                         }
        return JsonResponse(response_json)


def auth_Login(request):
    """
    用户登录
    :param request: 用户请求信息
    :return: JSON数据
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 前端传入的JSON数据
        except json.JSONDecodeError as err:
            state = 3000
            information = '无效数据！请检查前端传递的JSON数据是否按照标准JSON格式正确传入:\n' + str(err)
            response_json = {"state": state,
                             "info": information,
                             "responseTime": timezone.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')
                             }
            return JsonResponse(response_json)

        user_name = data.get('username')
        user_password = data.get('password')
        if not user_name:
            state = 1001
            information = '用户名不能为空'
            response_json = {"state": state,
                             "info": information,
                             "requestGet": {
                                 "name": user_name,
                                 "password": "invisible"
                                 },
                             "responseTime": timezone.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')
                             }
            return JsonResponse(response_json)
        else:
            try:
                user_obj = auth.authenticate(username=user_name, password=user_password)
            except Exception as err:  # 执行SQL查询出现错误
                state = 3001  # 用户名或密码获取错误
                information = str(err)

                user_value = ''
            else:
                if user_obj:  # 用户输入用户名与密码正确
                    state = 2002  # 状态码反馈信息，0000代表用户存在并且用户输入的用户名与密码匹配。其他状态码对应一种错误，具体错误请查看API说明文档，或者查看“info”反馈信息。
                    information = 'OK'  # 记录程序反馈详细信息，若程序未出错，则为“OK”；若出错。则记录出错详细信息，类似于控制台报错信息
                    auth.login(request, user_obj)  # 记录用户登录状态
                    user_dict = user_obj.__dict__
                    user_value = {}  # 来自数据库中的所有关于该用户的属性以及值
                    for user_key, user_v in user_dict.items():
                        if user_key == '_state' or user_key == 'backend':
                            continue
                        elif user_key == 'last_login' or user_key == 'date_joined':
                            # values = int(timezone.mktime(timezone.localtime(user_v).timetuple()))  # datetime转本地时间戳
                            values = timezone.localtime(user_v).timestamp()
                            user_value[user_key] = values
                        else:
                            user_value[user_key] = user_v


                else:
                    state = 1111  # 用户名或密码错误
                    information = '用户名或密码错误'
                    user_value = ''



            finally:
                response_json = {"state": state,
                                 "info": information,
                                 "requestGet": {
                                     "name": user_name,
                                     "password": "invisible"
                                     },
                                 "responseTime": timezone.localtime().strftime('%Y-%m-%d %H:%M:%S'),
                                 "responseFromeDatabase": user_value
                                 }

            return JsonResponse(response_json)
    else:
        state = 4004
        information = '请求方式错误"GET"'
        response_json = {"state": state,
                         "info": str(information),
                         "responseTime": timezone.strftime('%Y-%m-%d %H:%M:%S', timezone.localtime())
                         }
        return JsonResponse(response_json)


def auth_LogOUT(request):
    try:
        auth.logout(request)
    except Exception as err:
        state = 3002
        information = err
    else:
        state = 2003
        information = '用户已退出登录'
    finally:
        response_json = {"state": state,
                         "info": str(information),
                         "responseTime": timezone.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')
                         }
        return JsonResponse(response_json)


def update(request):
    # try:
    data = json.loads(request.body)
    print(data)
    username = data.get('username')
    record = UserTable.objects.get(username=username)
    print(record)
    information = data.get('information')
    new_username = information.get('usename')

    if new_username is not None:
        record.username = new_username
    new_password = information.get('password')
    if new_password is not None and new_password != 'qhixns8xgcb8dcbj8hcb5':
        print(new_password)
        record.set_password(new_password)
    new_sex = information.get('sex')
    if new_sex is not None:
        record.sex = new_sex
    new_age = information.get('age')
    if new_age is not None:
        record.age = new_age
    new_email = information.get('email')
    if new_email is not None:
        record.email = new_email
    record.save()
    context = serializers.serialize(
        "json",
        [record],
    )
    return JsonResponse(json.loads(context), safe=False)
