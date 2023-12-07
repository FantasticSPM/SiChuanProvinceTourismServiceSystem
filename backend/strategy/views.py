# from django.shortcuts import render
from django.http import JsonResponse
import json
from django.core import serializers
from .models import Strategy
from lxml import etree
import re
import requests
import time
from selenium import webdriver


def index(request):  # 攻略内容主页，将存放的攻略从数据库中取出使用
    keywords = request.POST.get('keywords')
    data = {}
    context = serializers.serialize(
        "json",
        Strategy.objects.filter(pname__contains=keywords),  # 数据库查询
    )

    data["data"]= json.loads(context)
    for i in data["data"]:
        i['fields']['img_url'] = i['fields']['img_url'].split(",")
    return JsonResponse(data, safe=False)


def liuliang(request):  # 客流量查询模块
    header = {
        "method": "GET",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400",
    }
    uli = 'https://www.jiuzhai.com/news/number-of-tourists'
    content = requests.get(uli, headers=header).text  # 提取未处理的数据文本

    e = etree.HTML(content)
    resultdata = e.xpath('//tr/td/text()')
    result = e.xpath('//tr/td/a/text()')

    data1 = []
    data2 = []

    for index, result1 in enumerate(resultdata):
        data1.append(result1.replace("\n", "").replace("\t", ""))
    while '' in data1:
        data1.remove('')
    filter(None, data1)

    for index, result2 in enumerate(result):
        data2.append(result2.replace("\n", "").replace("\t", ""))

    filter(None, data2)
    for i in range(20):
        data2[i] = re.search(r'\d+', data2[i]).group()  # 完成对数据的修剪处理操作
    result = dict(zip(data1, data2))
    # response = json.dumps(result)
    return JsonResponse(result)


def monitor(request):  # 客源数据监控功能模块
    try:
        # 创建浏览器实例
        option = webdriver.ChromeOptions()
    except:
        option = webdriver.EdgeOptions()
        get_googleChrome = False
    else:
        get_googleChrome = True  # 标记是否正确找到谷歌浏览器
    option.add_argument('--disable-blink-features=AutomationControlled')
    # 设置修改selenium的特征值，防止被检测到
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 设置无头模式，不显示可视化界面
    option.add_argument('--headless')
    # 设置用户代理
    option.add_argument(
        '--user-agent= Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 116.0.0.0 Safari / 537.36 Edg / 116.0.1938.69')

    # 加载浏览器驱动
    try:
        if get_googleChrome:
            driver = webdriver.Chrome(options=option)
        else:
            driver = webdriver.Edge(options=option)
    except:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager

        try:
            # 下载与电脑谷歌浏览器版本匹配的浏览器驱动程序
            if get_googleChrome:
                ChromeDriverManager().install()  # 对应谷歌浏览器
            else:
                EdgeChromiumDriverManager().install()  # 对应edge浏览器
            time.sleep(20)  # 等待20秒下载时间
        except:
            data_json = {'state': False,
                         '备注': '未找到支持的谷歌浏览器或Edege浏览器，请安装后重试',
                         0: None, 1: None
                         }
            return data_json
    # 设置浏览器窗口大小
    driver.set_window_size(1920, 1080)

    url = 'https://m.abatour.com/chart/#/4'
    driver.get(url)
    time.sleep(1)  # 确保网页加载出来
    try:
        sourcePage = driver.page_source

        e = etree.HTML(sourcePage)

        def remove(item):
            for i in item:
                if ' ' in item:
                    item.remove(' ')

        resultdata1 = e.xpath('//div[@class="leftPartItem"]//text()')  # 今日客源地前十

        resultdata2 = e.xpath('//div[@class="contentBody InnerDetail"]//text()')  # 今日游客年龄段

        resultdata3 = e.xpath('//div[@class="playerNum-m"]//text()')  # 购票数据

        resultdata4 = e.xpath('//div[@class="InnerDetail-m"]//text()')  # 今日票型售检详情

        remove(resultdata1)
        remove(resultdata2)
        remove(resultdata3)
        remove(resultdata4)

        response = {  # 将数据进行挑选和重组，将数据简化为直观的键值对
            "今日客源地前十": {
                resultdata1[i]: resultdata1[i+1] for i in range(1, 20, 2)
            },
            "各年龄": {
                resultdata2[i]: resultdata2[i+1] for i in range(0, 10, 2)
            },
            "游客类型": {
                resultdata2[i]: resultdata2[i+1] for i in range(10, 16, 2)
            },
            "检票数据": {
                resultdata3[i]: resultdata3[i+1]+resultdata3[i+2]+resultdata3[i+3]+resultdata3[i+4]+resultdata3[i+5]+resultdata3[i+6] for i in range(0, 21, 7)
            },
            "售票人数": {
                resultdata4[i]: resultdata4[i+1] for i in range(6, len(resultdata4), 3)
            },
            "检票人数": {
                resultdata4[i]: resultdata4[i+2] for i in range(6, len(resultdata4), 3)
            },
        }
        return JsonResponse(response)
    finally:
        driver.quit()  # 关闭后台浏览器
