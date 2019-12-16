# coding: utf-8
 
import requests
from bs4 import BeautifulSoup
import re
 
 
def getWeath(city_code):
    try:
#        print(city_code)
        url = 'http://www.weather.com.cn/weather/%s.shtml'%city_code
        ret = requests.get(url)
    except BaseException as e:
        print(e)
        return {}
 
    ret.encoding = 'utf-8'
    soup = BeautifulSoup(ret.text, 'html.parser')
    tagToday = soup.find('p', class_ = "tem")  #第一个包含class="tem"的p标签即为存放今天天气数据的标签
    try:
        temperatureHigh = tagToday.span.string  #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
    except AttributeError:
        temperatureHigh = tagToday.find_next('p', class_="tem").span.string  #获取第二天的最高温度代替
 
    temperatureLow = tagToday.i.string  #获取最低温度
    temperatureLow=temperatureLow[:-1]
    temperatureHigh=temperatureHigh+'°C'
    weather = soup.find('p', class_ = "wea").string #获取天气
    wind = soup.find('p', class_ = "win") #获取风力
    clothes = soup.find('li', class_ = "li3 hot") #穿衣指数
 
    #print('最低温度:' + temperatureLow)
    #print('最高温度:' + temperatureHigh)
    #print('天气:' + weather)
    #print('温度：'+temperatureLow +'-'+ temperatureHigh)
    #print('风力:' + wind.i.string)
    #print('穿衣:' + clothes.a.span.string + "," + clothes.a.p.string)
    fileHandle=open('weather.txt','w')
    fileHandle.write('天气:' + weather)
    fileHandle.write('\n温度：'+temperatureLow +'-'+ temperatureHigh)
    fileHandle.write('\n风力:' + wind.i.string)
    fileHandle.close()
    return {'温度':temperatureHigh + '/' + temperatureLow
    , '天气':weather
    , '风力':wind.i.string
    , '穿衣':clothes.a.span.string + ',' + clothes.a.p.string}
 
def strDic(dic):
    str_weather = ''
    for key in dic:
       str_weather += key + ':' + dic[key]
       str_weather += '\n'
    return str_weather
 
if __name__ == "__main__":
    wea_str = strDic(getWeath(101340102))
