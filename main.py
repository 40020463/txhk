from ast import While
import asyncio
from code import interact
# import urllib.request
from copy import deepcopy
from re import template
from tkinter import BROWSE
import cv2
import random
import re
import os
import sys

from pyppeteer import launch
from urllib import request
import json
import calendar

import time




async def get_dis(sid):
    print('sid666', sid666)
    bg11 = cv2.imread(sid + 'bg1.png', 0)  # 灰度读取
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bg22 = cv2.imread(sid + 'bg2.png', 0) 
    res = cv2.matchTemplate(bg11, bg22, cv2.TM_CCOEFF_NORMED)  # 使用cv2的平方差匹配法来取值 TM_CCO-EFF_NORMED (相关系数匹配法)
    print(res)
    value = cv2.minMaxLoc(res)[2][0]  # minMaxLoc() 在数组中找到全局最小和最大值


    # dis = int(value * 310 / 672) - 52 #计算距离差
    # dis = int(value * 313 / 680) - 52  # 计算距离差
    dis = int(value * 310 / 672) - 52  # 计算距离差
    os.remove(sid + 'bg1.png')
    os.remove(sid + 'bg2.png')
    os.remove(sid + 'img_template.png')
    return dis


# https://t.captcha.qq.com/cap_union_new_verify

async def main():  # 声明一个异步函数
    userDataDir = './userData'
    browser = await launch({'userDataDir': userDataDir, 'headless': False, 'args': ['--window-size=1024,768']})  # 启动浏览器
    While_count = 0  # 循环次数
    while While_count < 10:
        While_count = While_count + 1
        print('循环次数：' + str(While_count))
        # page = await browser.newPage()
        page = await browser.newPage() 
        await page.setViewport({'width': 1024, 'height': 768}) 

        page.on('response', lambda rep: asyncio.ensure_future(interact_response(rep)))  # 注册事件，拦截返回.
        page.on('request', lambda req: asyncio.ensure_future(interact_request(req)))  # 注册事件，拦截请求
        await page.waitFor(1000)  # 等待1秒
        url = sys.argv[1]
        print(url)
        # url='https://ssl.captcha.qq.com/template/wireless_mqq_captcha.html?style=simple&aid=16&uin=12345678&sid=7306228800855071334&cap_cd=yr19Q9Kk2AhuP2qUDv1c23XRo5WrAerr_1hVJtTcbKNhzoseWLROig**&clientype=1&apptype=2'
        sid = re.findall(r'&sid=(.*?)&', str(url))
        print('登录开始 sid', sid[0])
        global xbc
        xbc = sid[0]
        await page.goto(url)  # 跳转到登录页面
        print('等待页面加载完成')  # 获取页面标题
        await page.waitFor(2000)  # 等待1秒
        print('截取当前页面')

        print('处理验证码') 
        await page.waitFor(1000) 
        print('处理验证码2', sid666)
        dis = await get_dis(sid666)
        await page.waitFor(1000)  # 等待1秒
        x = 400
        y = 260
        await page.mouse.move(x, y)  # 鼠标移动到指定位置
        await page.mouse.down()  # 鼠标按下
        await page.mouse.move(x + dis + random.uniform(30, 33), y, {'steps': 30})  # 鼠标移动到指定位置
        await page.waitFor(random.randint(300, 700))
        await page.mouse.move(x + dis + 29, y, {'steps': 30})
        await page.mouse.up()  # 鼠标抬起
        await page.waitFor(3000)  # 等待1秒
        await page.close()


async def interact_request(interact_request):
    if 'https://t.captcha.qq.com/cap_union_prehandle' in interact_request.url:
        print('拦截到了1')
        # print(interact_request.url)
        # print(interact_request.postData)
        # print(interact_request.headers)


async def interact_response(interact_response):
    # print('测试',interact_response.url)

    if 'https://t.captcha.qq.com/cap_union_new_verify' in interact_response.url:
        # print('拦截到了2')
        # print(interact_response.url)
        resp = await interact_response.text()
        # resp1 = interact_response.request
        # sid1=resp1.headers

        print(resp)
        errorCode = re.findall(r'{"errorCode":"(.*?)","', resp)
        if errorCode[0] in '0':
            print('验证码正确')

            randstr = re.findall(r'"randstr":"(.*?)"', resp)
            print(randstr[0])
            ticket = re.findall(r'"ticket":"(.*?)","', resp)
            print(ticket[0])
            # sid = re.findall(r'&sid=(.*?)&', str(sid1))
            # print(sid[0])
            # ts = calendar.timegm(time.gmtime())
            # file = open('./结果/'+str(ts)+'.txt','w')
            file = open('./结果/' + xbc + '.txt', 'w')
            file.write(randstr[0] + '\n' + ticket[0])
            print('验证码正确randstr(' + randstr[0] + ')ticket(' + ticket[0] + ')')
            file.close()


        else:
            print('验证码识别错误')

    if 'https://t.captcha.qq.com/cap_union_prehandle' in interact_response.url:
        print('拦截到了3')
        # print(interact_response.url)
        resp = await interact_response.text()
        # print(resp)
        img_index = re.findall(r'img_index=1(.*?)"},', resp)
        print("img_index199", str(img_index[0]))
        sid = re.findall(r'image=(.*?)&sess', str(img_index[0]))
        print("img_index299", str(sid[0]))
        # print(globals())
        global sid666
        sid666 = str(sid[0])

        img_bg = 'https://t.captcha.qq.com/cap_union_new_getcapbysig?img_index=1' + str(img_index)
        request.urlretrieve(img_bg, './' + sid666 + 'bg1.png')  # 背景图片下载到本地

        img_template = 'https://t.captcha.qq.com/cap_union_new_getcapbysig?img_index=0' + str(img_index)
        request.urlretrieve(img_template, './' + sid666 + 'img_template.png')  # 背景图片下载到本地

        file_path = './' + sid666 + 'img_template.png'  # 图片路径
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        x, y, w, h = (141, 490, 119, 118)
        crop = img[y:y + h, x:x + w]
        # im = im[100:5,115:250]
        save_path = r'./'
        out_file_name = sid666 + 'bg2'
        save_path_file = os.path.join(save_path, out_file_name + '.png')
        cv2.imwrite(save_path_file, crop)
        print('保存图片')



asyncio.get_event_loop().run_until_complete(main())
