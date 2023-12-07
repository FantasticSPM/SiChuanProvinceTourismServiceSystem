# Create your tests here.
import json

from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest

from .models import UserTable


# 跳过CSRF
# from django.views.decorators.csrf import csrf_exempt


# 注册处理函数
def SLogin(request):
    # print(request.POST)
    if request.method == 'POST':
        # # 方法一 直接通过根据html页面中标签属性获取值
        # user_name = request.POST.get('username', '')  # 获取name属性为username的值
        # user_password = request.POST.get('password', '')  # 获取name属性为password的值，以下get雷同
        # user_xb = request.POST.get('user_xs', '')

        # 方法二 前端使用JSON形式传入数据，通过获取JSON中的键值对获取值
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(['False', '无效的数据'])
        user_name = data.get('username', '')  # 获取username的值
        user_password = data.get('password', '')  # 获取password的值，以下get雷同
        user_xb = data.get('user_xs', '0')

        if int(user_xb) == 0 or user_xb == '男':  # 接受两种传入值的方法：1.0/1: 男/女;2.直接传入字符串男/女
            user_xb = '男'
        else:
            user_xb = '女'

        # # 获取年龄信息，要求传入值只能包含数字
        # def get_age(input_age):
        #     if isinstance(obj, class_or_tuple) input_age
        try:
            user_age = int(data.get('user_age', '0'))
        except:
            user_age = 0

        if not user_name:
            msgage = '用户名不能为空'
            state = 'False'  # 记录SQL查询反馈信息，OK代表成功，False代表失败
            information = msgage  # 记录查询详细信息，若查询未出错，则为1；若出错。则记录出错详细信息，类似于控制台报错信息。这里为报错JSON数据完整性，这里设置为msgage
        else:
            user1 = UserTable(user_name=user_name, user_age=int(user_age), user_password=user_password, user_xs=user_xb)
            try:
                user1.save()
                state = 'OK'
                information = 1  # 记录查询详细信息，若查询未出错，则为1；若出错。则记录出错详细信息，类似于控制台报错信息
                msgage = '注册成功！'  # 执行SQL语句后返回信息
            except Exception as err:
                state = 'False'
                information = err
                # print('错误：', information, '\n', type(information))
                msgage = '注册失败！'
        response_json = {"state": state,
                         "info": str(information),
                         "user_Web_get": {
                             "name": user_name,
                             "password": user_password,
                             "age": user_age,
                             "sex": user_xb
                             },
                         "register_return_information": msgage
                         }
        # print(response_json, '\n', type(response_json))
        return JsonResponse(response_json)
    else:
        state = 'False'
        information = '请求方式错误"GET"'
        msgage = information
        response_json = {"state": state,
                         "info": str(information),
                         "register_return_information": msgage
                         }
        return JsonResponse(response_json)


# 登录处理函数
# @csrf_exempt # 取消CSRF保护
def Login(request):
    if request.method == 'POST':
        try:
            # print(request.body)
            data = json.loads(request.body)  # 前端传入的JSON数据
            # print(data)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(['False', '无效的数据'])

        user_name = data.get('username')
        user_password = data.get('password')
        try:
            reapons = UserTable.objects.filter(user_name=user_name)  # 查询数据库返回值
            state = "OK"  # 记录查询反馈信息，OK代表成功，False代表失败
            information = 1  # 记录查询详细信息，若查询未出错，则为1；若出错。则记录出错详细信息，类似于控制台报错信息
        except Exception as err:  # 执行SQL查询出现错误
            reapons = None
            state = "False"
            information = err
        finally:
            if reapons:
                response_json = json.loads(serializers.serialize('json', reapons))[0]
            else:
                response_json = None  # 查无此人！SQL语言正常执行，但是数据库中并没有数据，用户未注册！
            response_json = {"state": state,
                             "info": information,
                             "user_Web_get": {
                                 "name": user_name,
                                 "password": user_password
                                 },
                             "database_SQL_get": response_json
                             }

        # print(response_json, '\n', type(response_json))
        return JsonResponse(response_json)
    else:
        state = 'False'
        information = '请求方式错误"GET"'
        msgage = information
        response_json = {"state": state,
                         "info": str(information),
                         "register_return_information": msgage
                         }
        return JsonResponse(response_json)


# 测试get
def get_test(request):
    try:
        # print(request.GET)
        data = request.GET  # 前端传入的数据
        # print(data)
    except Exception:
        return HttpResponseBadRequest(['False', '无效的数据'])
    else:
        user_name = data.get('username')
        user_password = data.get('password')
        response_json = {
            "username": user_name,
            "userpassword": user_password,
            "message": "GET方法返回值"
            }
        # print(response_json, type(response_json))
        return JsonResponse(response_json)

# 使用django自带的功能实现用户注册与登录
