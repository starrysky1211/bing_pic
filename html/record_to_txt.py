import urllib
import json
import wave
import base64
import os
import subprocess

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




os.system('ffmpeg -i a.mp3 -ar 16000 -ac 1 -acodec pcm_s16le record.wav')

wav_to_text('a.wav')

os.remove('a.wav')
