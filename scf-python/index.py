# -*- coding: utf8 -*-
import json
import requests, json, time, os, sys
cookie = os.getenv("COOKIE_SMZDM")
key = os.getenv("PUSH_TOKEN")

def main(cookie):
    try:
        msg = ""
        s = requests.Session()
        s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'})
        t = round(int(time.time() * 1000))
        url = f'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin?_={t}'
        headers = {
            "cookie" : cookie.encode("utf-8"),
            'Referer': 'https://www.smzdm.com/'
            }
        r = s.get(url, headers=headers, verify=False)
        if r.json()["error_code"] != 0:
            msg += "smzdm cookie失效"
        else:
            msg += "smzdm签到成功"
    except Exception as e:
        print('repr(e):', repr(e))
        msg += '运行出错,repr(e):'+repr(e)
    return msg + "\n"

def smzdm_pc():
    msg = ""
    global cookie
    if "\\n" in cookie:
        clist = cookie.split("\\n")
    else:
        clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += main(cookie)
        i += 1
    push(msg)
    return msg

#push
def push(text):
    headers = {
        "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent":"MiFit/4.6.0 (iPhone; iOS 14.0.1; Scale/2.00)"
    }
    try:
        url = "http://www.pushplus.plus/send?token=" + key + "&title=什么值得买&content=" + f'{text}' + "&template=html"
        r = requests.get(url,headers=headers)
        print(r.text)
    except:
        print("发送失败！")
    else:
        print("发送成功！")    
        
def main_handler(event, context):
    smzdm_pc()
    return("Hello World")
