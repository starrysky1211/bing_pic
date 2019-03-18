
# __*__ coding: UTF-8 __*__
from wxpy import *
import sqlite3
import random
import time
import requests
import time
import os
import urllib

import json
import wave
import base64
import subprocess


def baidu_weather_api(msg):
    res = msg.split()[1]
    url='http://api.map.baidu.com/telematics/v3/weather?location=res&ak=8yoeZq9BzQGxKQMvpUyKNZuZ&output=json'
    url = url.replace('res', res)
    condition = requests.get(url).content
    condition = str(condition,encoding='utf8')
    condition = json.loads(condition)
    data = condition["results"][0]

    current_city = '当前城市：'+ data["currentCity"]+'\n'
    pm = "PM2.5为："+data["pm25"]+'\n'

    today_tem=data["weather_data"][0] # dict

    tem_today = "今日温度：" + today_tem["temperature"] + '\n'
    weather_today = "天气："+today_tem['weather']+'\n'
    wind = "风力："+today_tem["wind"]+'\n'
    now = today_tem["date"]+'\n'

    segestions = data["index"]
    segestion = ''
    for se in segestions:
        if se['title'] == '穿衣':
            segestion += "衣着推荐："+se['des']+'\n\n'
        if se['title'] == "紫外线强度":
            segestion += se['des'] + '\n'

    reply=current_city+pm+tem_today+weather_today+wind+now+segestion
    return reply


def getBGURL():
    print('in getBGURL')
    thing = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN')
    thing = thing.json()
    bgurl = thing["images"][0]["url"]
    bgurl = "https://cn.bing.com/"+bgurl
    details = thing["images"][0]["copyright"]
    story_url = thing["images"][0]["copyrightlink"]
    return bgurl, details, story_url


def down_bing_pic():
    date = time.strftime('%Y_%m_%d', time.localtime(time.time()))
    print(-1)
    with open('bing_flag.txt','rb') as ff:
        thing = ff.readlines()
        print(-1.2)
        for tid, de in enumerate(thing):
            print(-1,tid)
            thing[tid] = str(de,encoding='utf8')
    if thing[0]==date:
        print(1)
        return thing[1], thing[2]
    print(0)
    url, details, story = getBGURL()
    print(1)
    pic = requests.get(url).content
    p_name = "today_bing.jpg"
    print('downloading bing_pic today')
    with open('bing_flag.txt','wb') as ff:
        string = date+'\n'+details+'\n'+story
        ff.write(bytes(string, encoding='utf8'))
    with open(p_name,'wb') as f:
        f.write(pic)
    return details, story


# 初始化微信机器人
bot = Bot(cache_path=True)

wife = ensure_one(bot.friends().search("我家的小"))
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


home = ensure_one(bot.groups().search('皇室'))

@bot.register(msg_types=TEXT)
def reply_massage(msg):
    print(msg)
    if msg.text in ['bing', '必应']:
        # 读取背景图片url并保存在S:\master\self_learning\Python\learn-python\bing_pic\html\****_**_**.jpg中
        p_name = "today_bing.jpg"
        details, story = down_bing_pic()
        msg.reply(details)
        msg.reply_image(p_name)
        msg.reply("详情点击："+story)
    if "天气预报" in msg.text[:5]:
        mes = msg.text
        if len(mes.split()) == 1:
            mes='天气预报 北京海淀'
        condition = baidu_weather_api(mes)
        msg.reply(condition)
    # if flag<0.1:
    #     print("turing replying")
    #     reply = tuling.reply_text(msg)
    #     msg.reply('[bot]'+reply)
    # database = sqlite3.connect(r'E:\cloud\home\wxRobot\repeat.db')
    # db = database.cursor()
    # cursor = db.execute('SELECT ID, WORDS, REPLY FROM keywords')
    # for row in cursor:
    #     if row[1] in msg.text:
    #         msg.reply(row[2])
    #     elif '添加词条' in msg.text:
    #         thing = msg.text.split()
    #         db.execute("SELECT WORDS FROM keywords where WORDS = '%s'" % thing[1])
    #         exist = db.fetchall()
    #         if len(exist) > 0:
    #             break
    #         else:
    #             db.execute("INSERT INTO keywords (ID, WORDS, REPLY) \
    #                 VALUES ((SELECT max(Id) FROM keywords)+1 ,'%s','%s')" % (thing[1], '[bot]'+thing[2]))
    #             msg.reply('添加成功')
    #             break
    # db.close()
    # database.commit()
    # database.close()


@bot.register(msg_types=RECORDING)
def translate_sound(msg):
    msg.get_file(save_path='record.mp3')
    # path = os.path.abspath('.')+'\\'
    # print(path)
    try:
        subprocess.check_call('ffmpeg -i record.mp3 -ar 16000 -ac 1 -acodec pcm_s16le record.wav', shell=True)
        # ''
    except Exception as e:
        print(1, e)
    wav_to_text('a.wav')
    try:
        os.remove('a.wav')
    except Exception as e:
        print(e)


embed()
