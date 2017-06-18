from wxpy import *
import sqlite3
import time
import urllib.request, urllib.parse, urllib.error
import time
import os


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
    filename = path+'\\'+date+'.jpg'
    return filename



# 初始化微信机器人
bot = Bot()

wife = ensure_one(bot.friends().search("甜甜圈"))
tuling = Tuling(api_key='4e6c2cd5858647ea9851346c8ecac433')


@bot.register(wife, TEXT)
def print_messages(msg):
    print(msg)
    # tuling.do_reply(msg)
    database = sqlite3.connect(r'S:\家\wxRobot\repeat.db')
    db = database.cursor()
    cursor = db.execute('SELECT ID, WORDS, REPLY FROM keywords')
    for row in cursor:
        if row[1] in msg.text:
            msg.reply(row[2])
            break
        elif '添加词条' in msg.text:
            thing = msg.text.split()
            db.execute("SELECT WORDS FROM keywords where WORDS = '%s'" % thing[1])
            exist = db.fetchall()
            if len(exist) > 0:
                break
            else:
                db.execute("INSERT INTO keywords (ID, WORDS, REPLY) \
                    VALUES ((SELECT max(Id) FROM keywords)+1 ,'%s','%s')" % (thing[1], '[bot]'+thing[2]))
                msg.reply('添加成功')
                break
    db.close()
    database.commit()
    database.close()


home = ensure_one(bot.groups().search('皇室'))


@bot.register(home, TEXT)
def reply_massage(msg):
    print(msg)
    if msg.text == 'bing' or '必应':
        # 读取背景图片url并保存在S:\master\self_learning\Python\learn-python\bing_pic\html\****_**_**.jpg中
        url = getBGURL()
        html = urllib.request.urlretrieve(url, filename=name())
        msg.reply_image(time.strftime('%Y_%m_%d', time.localtime(time.time()))+'.jpg')
    # tuling.do_reply(msg)
    database = sqlite3.connect(r'S:\家\wxRobot\repeat.db')
    db = database.cursor()
    cursor = db.execute('SELECT ID, WORDS, REPLY FROM keywords')
    for row in cursor:
        if row[1] in msg.text:
            msg.reply(row[2])
            break
        elif '添加词条' in msg.text:
            thing = msg.text.split()
            db.execute("SELECT WORDS FROM keywords where WORDS = '%s'" % thing[1])
            exist = db.fetchall()
            if len(exist) > 0:
                break
            else:
                db.execute("INSERT INTO keywords (ID, WORDS, REPLY) \
                    VALUES ((SELECT max(Id) FROM keywords)+1 ,'%s','%s')" % (thing[1], '[bot]'+thing[2]))
                msg.reply('添加成功')
                break
    db.close()
    database.commit()
    database.close()


embed()
