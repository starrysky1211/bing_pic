import requests
import csv
import json

# 百度天气API调用
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
            segestion += "衣着推荐："+se['des']+'\n'
        if se['title'] == "紫外线强度":
            segestion += se['des'] + '\n'

    reply=current_city+pm+tem_today+weather_today+wind+now+segestion
    return reply




# 中国天气网API调用
def china_weather_web_api(msg):
    with open('city_code.json','r', encoding='UTF-8') as f:
        cc = json.loads(f.read())
    pro_list = cc['CityCode'] # list of 34 province
    desire_list = msg.split()[1:]
    dcity, dcontry = '', ''
    if len(desire_list) == 1:
        # 只有城市名，没有区名，只搜索城市code
        dcity=desire_list[0]
        dcontry = desire_list[0]
    else:
        # 城市名区名都有
        dcity=desire_list[0]
        dcontry = desire_list[1]
    # 找城市
    cou_list = []
    for pro in pro_list:
        city_list = pro["cityList"] # list of every city in each province
        for city in city_list: # dict of info of one city
            if dcity in city["cityName"]:
                cou_list = city["countyList"]
                break
    # 拿编号
    res = ''
    for country in cou_list:
        if dcontry in country['name']:
            res = country["code"]
            break

    # 爬取天气情况
    url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=res'
    url = url.replace('res', res)
    condition = requests.get(url).content
    return str(condition,encoding='utf8')

if __name__ == "__main__":
    condition = baidu_weather_api("天气预报 北京海淀")
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
            segestion += "衣着推荐："+se['des']+'\n'
        if se['title'] == "紫外线强度":
            segestion += se['des'] + '\n'

    reply=current_city+pm+tem_today+weather_today+wind+now+segestion
    print(reply)

    


# 高德API调用 ，没有预报，只有实时？
# url = 'https://restapi.amap.com/v3/weather/weatherInfo?city=adnode&key=2d41342b512acfb60e41aa6dd67c1031'

# import json
# with open('city_adnode.json','r') as f:
#     ad = json.loads(f.read())

# msg='天气预报 北京'
# try:
#     dc, da = msg.split()[1:]
# except:
#     dc = msg.split()[1]
#     da = ''
# res = ''
# flag = 0
# for city in ad:
#     if dc in city:
#         areas = ad[city]
#         for area in areas:
#             if da in area:
#                 res=areas[area]
#                 flag = 1
#                 break
#         if not flag:
#             res = areas['origin']
#     break
# print(type(res))
# url = url.replace('adnode',res)
# print(url)
# addition = requests.get(url).json()
# print(addition)


# 转换csv至json文件
# ad_dict={}
# ccode_l=''
# city_n=''
# with open('AMap_adcode_citycode.csv','r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         ccode=row[2]
#         if ccode != ccode_l:
#             ad_dict[row[0]]={'origin':row[1]}
#             city_n=row[0]
#             ccode_l=ccode
#         else:
#             ad_dict[city_n][row[0]]=row[1]
# import json
# jad = json.dumps(ad_dict)
# with open('city_adnode.json','w') as f:
#     f.write(jad)