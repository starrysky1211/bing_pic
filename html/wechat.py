from wxpy import *
import sqlite3

import time
import urllib.request, urllib.parse, urllib.error
import time
import os

import json
import wave
import base64
import subprocess


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
bot = Bot(cache_path=True)

wife = ensure_one(bot.friends().search("甜甜圈"))
tuling = Tuling(api_key='4e6c2cd5858647ea9851346c8ecac433')


# 调用百度语音识别API
def get_token():
    URL = 'http://openapi.baidu.com/oauth/2.0/token'
    _params = urllib.parse.urlencode({'grant_type': b'client_credentials',
                                'client_id': b'BzsS5AEEC6qspN51baBKCwmf',#改成你自己的
                                'client_secret': b'TG0RcHZOuUq0wGrZdwFycq619v3gQxNb'})#改成你自己的
    _res = urllib.request.Request(URL, _params.encode())
    _response = urllib.request.urlopen(_res)
    _data = _response.read()
    _data = json.loads(_data)
    return _data['access_token']


def wav_to_text(wav_file):
    try:
        wav_file = open(wav_file, 'rb')
    except IOError:
        print('文件错误啊，亲')
        return
    wav_file = wave.open(wav_file)
    n_frames = wav_file.getnframes()
    print('n_frames ', n_frames)
    frame_rate = wav_file.getframerate()
    print("frame_rate ", frame_rate)
    if n_frames == 1 or frame_rate not in (8000, 16000):
        print('不符合格式')
        return
    audio = wav_file.readframes(n_frames)
    seconds = n_frames/frame_rate+1
    minute = int(seconds/60 + 1)
    for i in range(0, minute):
        sub_audio = audio[i*60*frame_rate:(i+1)*60*frame_rate]
        base_data = base64.b64encode(sub_audio)
        data = {"format": "wav",
                "token": get_token(),
                "len": len(sub_audio),
                "rate": frame_rate,
                "speech": base_data.decode(),
                "cuid": "B8-AC-6F-2D-7A-94",
                "channel": 1}
        data = json.dumps(data)
        res = urllib.request.Request('http://vop.baidu.com/server_api',
                              data.encode(),
                              {'content-type': 'application/json'})
        response = urllib.request.urlopen(res)
        res_data = json.loads(response.read())
        try:
            print(res_data['result'][0])
        except Exception as e:
            print(e)


@bot.register(wife, TEXT)
def print_messages(msg):
    print(msg)
    # tuling.do_reply(msg)
    database = sqlite3.connect(r'D:\cloud\家\wxRobot\repeat.db')
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
    # if msg.text == 'bing' or '必应':
    #     # 读取背景图片url并保存在S:\master\self_learning\Python\learn-python\bing_pic\html\****_**_**.jpg中
    #     url = getBGURL()
    #     html = urllib.request.urlretrieve(url, filename=name())
    #     msg.reply_image(time.strftime('%Y_%m_%d', time.localtime(time.time()))+'.jpg')
    reply = tuling.reply_text(msg)
    msg.reply('[bot]'+reply)
    database = sqlite3.connect(r'D:\cloud\家\wxRobot\repeat.db')
    db = database.cursor()
    cursor = db.execute('SELECT ID, WORDS, REPLY FROM keywords')
    for row in cursor:
        if row[1] in msg.text:
            msg.reply(row[2])
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


@bot.register(wife, RECORDING)
def translate_sound(msg):
    msg.get_file(save_path='a.mp3')
    path = os.path.abspath('.')+'\\'
    print(path)
    try:
        subprocess.check_call('ffmpeg -i a.mp3 -ar 16000 -ac 1 -acodec pcm_s16le a.wav', shell=True)
        # ''
    except Exception as e:
        print(1, e)
    wav_to_text('a.wav')
    try:
        os.remove('a.wav')
    except Exception as e:
        print(e)




lab = ensure_one(bot.groups().search("精密机电小分队"))
@bot.register(lab, TEXT)
def reply_auto(msg):
    print(msg)
    # if msg.text == 'bing' or '必应':
    #     # 读取背景图片url并保存在S:\master\self_learning\Python\learn-python\bing_pic\html\****_**_**.jpg中
    #     url = getBGURL()
    #     html = urllib.request.urlretrieve(url, filename=name())
    #     msg.reply_image(time.strftime('%Y_%m_%d', time.localtime(time.time()))+'.jpg')
    tuling.do_reply(msg)
    database = sqlite3.connect(r'D:\cloud\家\wxRobot\repeat.db')
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
