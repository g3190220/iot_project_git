import json, requests
import pprint  
from hanziconv import HanziConv
def Taoyuan():
    weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city=桃园"  #将链接定义为一个字符串
    response = requests.get(weatherJsonUrl)      #获取并下载页面，其内容会保存在respons.text成员变量里面
    response.raise_for_status()
    weatherData = json.loads(response.text)
    # pprint.pprint(weatherData)
    content=""
    w = weatherData['data']
    location_="地點：%s" % HanziConv.toTraditional(w['city'])
    print(location_)
    
    #日期
    date_a = []
    #最高温和最低温
    highTemp = []
    lowTemp = []
    #天氣
    weather = []
    #进行五天的天气遍历
    # for i in range(0):
    date_a.append(w['forecast'][0]['date'])
    highTemp.append(w['forecast'][0]['high'])
    lowTemp.append(w['forecast'][0]['low'])
    weather.append(w['forecast'][0]['type'])
    #输出
    date_="日期：" + HanziConv.toTraditional(date_a[0])
    maxmin_temp_="溫度：最" + HanziConv.toTraditional(lowTemp[0]) + '  最' + HanziConv.toTraditional(highTemp[0])
    weather_="天氣：" + HanziConv.toTraditional(weather[0])

    description_="今日適合穿著：" + HanziConv.toTraditional(w['ganmao'])
    temp_now_="當前溫度：" + HanziConv.toTraditional(w['wendu']) + "℃"
    # print(date_)
    # print(maxmin_temp_)
    # print(weather_)
    # print(description_)
    # print(temp_now_)
    content=(date_
            +"\n"+maxmin_temp_
            +"\n"+weather_
            +"\n"+description_
            +"\n"+temp_now_)
    return content


