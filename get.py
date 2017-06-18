# coding:utf-8

import urllib.request, urllib.parse, urllib.error
import time
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


def getBGURL():
    thing = getHtml('https://www.bing.com')
    bgurl = thing[thing.index(b'g_img={url:')+12:len(thing)]
    bgurl = bgurl[0:bgurl.index(b',id:')-1]
    bgurl = bgurl.replace(b'"', b'')
    bgurl = 'https://www.bing.com'+bgurl.decode('utf-8')
    return bgurl


def name():
    path = os.path.dirname(os.path.realpath(__file__))
    date = time.strftime('%Y_%m_%d', time.localtime(time.time()))
    filename = path+'\html\\'+date+'.jpg'
    return filename

# 读取背景图片url并保存在S:\master\self_learning\Python\learn-python\bing_pic\html\****_**_**.jpg中
url = getBGURL()
html = urllib.request.urlretrieve(url, filename=name())
# 将图片使用163邮箱发送出去
username = '15652826118@163.com'
password = open('password.txt').readline()

receivers = ','.join(['lintsung@yeah.net', 'lcz9989@126.com'])

msg = MIMEMultipart()
msg["Subject"] = time.strftime('year:%Y-month:%m-date:%d', time.localtime(time.time()))+' Bing Today'
msg['From'] = username
msg['To'] = receivers

text = MIMEText("This is Bing Today, hope you a good mood!!")
msg.attach(text)

jpg = MIMEApplication(open(name(), 'rb').read())
jpg.add_header('Content-Disposition', 'attachment', filename='picture.jpg')
msg.attach(jpg)

try:
    client = smtplib.SMTP()
    client.connect('smtp.163.com')
    client.login(username, password)
    client.sendmail(username, receivers, msg.as_string())
    client.quit()
    print('带有必应今日美图的邮件发送成功！')
except smtplib.SMTPRecipientsRefused:
    print('Recipient refused')
except smtplib.SMTPAuthenticationError:
    print('Auth error')
except smtplib.SMTPSenderRefused:
    print('Sender refused')
except smtplib.SMTPException as e:
    print(e)



