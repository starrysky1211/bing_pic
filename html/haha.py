import urllib.request as urllib
import time
import os


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getBGURL():
    thing = getHtml('https://www.bing.com')
    bgurl = thing[thing.index('g_img={url:')+12:len(thing)]
    bgurl = bgurl[0:bgurl.index(',id:')-1]
    bgurl = bgurl.replace('"', '')
    bgurl = 'https://www.bing.com'+bgurl
    return bgurl


def name():
    path = os.path.dirname(os.path.realpath(__file__))
    date = time.strftime('%Y_%m_%d', time.localtime(time.time()))
    filename = path+'\\'+date+'.jpg'
    return filename


# 读取背景图片url并保存在S:\master\self_learning\Python\learn-python\bing_pic\html\****_**_**.jpg中
def do():
    url = getBGURL()
    html = urllib.urlretrieve(url, filename=name())
    return 0
do()
