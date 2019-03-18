# __*__ coding: UTF-8 __*__
import requests
import time
import os


# def getHtml(url):
#     page = urllib.urlopen(url)
#     html = page.read()
#     return html


def getBGURL():
    thing = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN')
    thing = thing.json()
    bgurl = thing["images"][0]["url"]
    bgurl = "https://cn.bing.com/"+bgurl
    return bgurl


def name():
    date = time.strftime('%Y_%m_%d', time.localtime(time.time()))
    filename = date+'.jpg'
    return filename


# 读取背景图片url并保存在S:\master\self_learning\Python\learn-python\bing_pic\html\****_**_**.jpg中
def do():
    url = getBGURL()
    pic = requests.get(url).content
    p_name = name()
    if os.path.exists('bing/'+p_name):
        print("existed")
        return
    with open('bing/'+p_name,'wb') as f:
        f.write(pic)
    print("downloaded")


do()
