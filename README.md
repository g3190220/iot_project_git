# SmartNote
### 構想
SmartNote能夠清楚顯現承辦人現在的狀況，比如是暫時離開10分鐘、或是下午才上班、甚至是今天請假等等資訊，都能夠讓來辦公室的人，比較不會因沒找到人而感到迷茫，不知道應該繼續等或著是改天再來辦事情。只要擁有「SmartNote」這項兼具美觀性及實用性的工具，上述的情況便能迎刃而解。而且，平常在座位上時，也可以當作時鐘、鬧鐘來使用，上面顯示今日的日期時間、天氣；甚至可以當作臨時便條，隨手記下一些事情來提醒自己，所以這是一項非常適合白領，很便利的辦公室智慧小物。使用者隨時都能夠自己用手機更改欲顯示的資訊，利人利己，也讓工作更有效率。
<br>額外小功能：網頁鬧鐘(網頁設定時間，時間到了連接的蜂鳴器會發出聲響提醒，墨水屏也會顯示畫面提示)<br>
* 主要構想參考資料：<br>
* https://www.jianshu.com/p/11de23140d10<br>
* https://blog.csdn.net/kim5659/article/details/102835977<br>
* 影片連結<br>
* https://youtu.be/6l6oUawLiOg<br>
### 材料
* Raspberry pi *1
* 296x128, 2.9inch E-Ink display module *1 (亦稱為墨水屏)
* Touch 觸摸感測器模組 1路觸摸開關傳感器  *1
* DHT22/AM2302溫濕度感測器 *1
* 蜂鳴器 *1
### 步驟一、連接基本相關設備(墨水屏、touch sensor、DHT22/AM2302溫濕度感測器、蜂鳴器)
樹梅派GPIO參考:https://pinout.xyz/pinout/pin4_5v_power<br>
以下數字以BCM為主
* 墨水屏：<br>
參考資料:http://www.waveshare.net/wiki/2.9inch_e-Paper_Module<br>
請對照參考資料網址的表格相對應連接<br>
* touch sensor:<br>
參考資料:http://kookye.com/2017/06/01/design-a-touch-switch-through-a-raspberry-pi-board-and-digital-touch-sensor/<br>
VCC ： 5V<br>
SIG ： 27<br>
GND ： ground<br>
* DHT22/AM2302溫濕度感測器：<br>
參考資料：https://kingfff.blogspot.com/2018/05/raspberry-pi-3-model-bdht22.html<br>
VCC ： 5V<br>
DAT ： 4<br>
NC ： 不用接<br>
GND ： ground<br>
* 蜂鳴器：<br>
接在麵包板上，正極pin腳連到12
### 步驟二、安裝設定 2.9inch E-Ink display module
詳細指令參考資料:http://www.waveshare.net/wiki/2.9inch_e-Paper_Module<br>
1. 開啟SPI接口<br>
2. 重啟樹莓派<br>
3. 安裝BCM2835<br> 
4. 安装wiringPi<br>
5. 安装所需Python套件(pip、pil、numpy、RPi.GPIO、spidev等等，詳細請看參考資料)<br>
3. 去git可下載官方測試程式，執行墨水屏對應版本py檔(本專案版本為epd2in9.py)，若成功顯示畫面則代表安裝設定完成<br>
### 步驟三、顯示日期時間並結合溫溼度感測計之資料傳到墨水屏上顯示頁面
* 顯示日期時間，且秒數為局部刷新<br>
參考資料：官方的測試程式(epd2in9.py)<br>
局部刷新的功能，大致邏輯是以每秒部分畫面剪下貼上的方式來執行，以下為相關程式碼擷取：
```python
time_draw.rectangle((10, 10, 120, 50), fill = 0)
time_draw.text((10, 15), time.strftime('%H:%M:%S'), font = font24, fill = 255)
newimage_3 = time_image.crop([10, 10, 120, 50])
time_image.paste(newimage_3, (10,15))
```
* 溫溼度感測計之資料傳到墨水屏上<br>
參考資料：https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/<br>
以下為相關程式碼擷取：
```python
# get data from DHT sensor
def getDHTdata():
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum 
```

```python
#溫溼度計
temp, hum = getDHTdata()
temp_val=str(temp)
hum_val=str(hum)

time_draw.rectangle((195, 85, 235, 20), fill = 255)
time_draw.text((144, 19), "Temp: "+temp_val+" *C", font = font18, fill = 0) 
time_draw.text((144, 55), "Hum : "+hum_val+" %", font = font18, fill = 0)
                        
newimage_1 = time_image.crop([195, 85, 235, 20])
time_image.paste(newimage_1, (144, 19))  
```


### 步驟四、透過touch sensor來讓墨水屏顯示日期時間頁面或暫停此功能
參考資料：https://www.itread01.com/content/1548642622.html
1. 透過判斷touch sensor的高低電位來判斷是否碰觸，碰觸後觸發顯示日期時間的方法<br>
```python
while True:
		if GPIO.input(TouchPin) == GPIO.LOW:
			print("wait to touch...")
				
		else:
			print ('you touched!')
			epd_2in9.getDHTdata()
			epd_2in9.showtime()
```
2. 方法執行後，作add_event_detect，當判斷到有電位差便會執行close_epd的方法，使本來迴圈暫停<br>
3. close_epd的方法裡要有remove_event_detect，要不然無法重複啟動或關閉<br>
*詳細程式碼請看epd_2in9.py

### 步驟五、製作網頁，並運用FLASK技術作網頁後端伺服器
參考資料：<br>
* https://kknews.cc/zh-tw/tech/yy6pg5j.html<br>
* https://zhuanlan.zhihu.com/p/49748475
### 步驟六、將使用者輸入的資料從前端傳到FLASK，再透過墨水屏顯示
參考資料：<br>
* https://www.maxlist.xyz/2019/03/17/flask-get-post/<br>
* https://www.lagou.com/lgeduarticle/70803.html<br>
需import以下Python套件，主要是以post方式從前端傳回flask
```python
from flask import Flask,flash, render_template,request,jsonify
```
### 步驟七、製作網頁鬧鐘，並將時間與樹梅派同步，並讓蜂鳴器與墨水屏同步提示
參考資料：<br>
* https://www.google.com/search?biw=1422&bih=642&ei=s0kPXoaJLsvEmAW4xYCwBQ&q=timepicker+git&oq=timep+git&gs_l=psy-ab.1.0.0i7i30l2j0i8i7i10i30l2j0i7i5i10i30.28557.29946..31887...0.0..0.61.320.6......0....1..gws-wiz.......0i7i10i30j0i13j0i13i10j0.pnN0HpEG4Rw<br>
* https://github.com/aschepis/jquery-timepicker<br>
___
* 網頁鬧鐘，主要是運用已有的套件jquery timepicker來做<br>
* 將設定時間傳回FLASK，墨水屏改變顯示畫面<br>
* 當時間到墨水屏更顯示畫面，蜂鳴器也發出聲響<br>
* 此方法詳細程式碼請看sketch.py裡的control_led()方法<br>

### 步驟八、將溫溼度的資料數值傳到網頁上顯示
參考資料：<br>
* https://raspberrypi.readbook.tw/python-flask.html<br>
* http://shumeipai.nxez.com/2018/07/03/video-streaming-web-server-with-flask.html<br>
以下為相關程式碼：

```python
# get data from DHT sensor
def getDHTdata():
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum
#將資料以物件的方式傳回網頁
@app.route('/t_h_data/')
def t_h_submit():
    timeNow = time.asctime( time.localtime(time.time()) )
    temp, hum = getDHTdata()
    templateData = {
        'time': timeNow,
        'temp': temp,
        'hum' : hum
    }
    return render_template('SmartNote.html',**templateData)
```
### 完成上述步驟，即可完成本次專案之功能。
