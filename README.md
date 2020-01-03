# SmartNote
### 構想
SmartNote能夠清楚顯現承辦人現在的狀況，比如是暫時離開10分鐘、或是下午才上班、甚至是今天請假等等資訊，都能夠讓來辦公室的人，比較不會因沒找到人而感到迷茫，不知道應該繼續等或著是改天再來辦事情。只要擁有「SmartNote」這項兼具美觀性及實用性的工具，上述的情況便能迎刃而解。而且，平常在座位上時，也可以當作時鐘、鬧鐘來使用，上面顯示今日的日期時間、天氣；甚至可以當作臨時便條，隨手記下一些事情來提醒自己，所以這是一項非常適合白領，很便利的辦公室智慧小物。使用者隨時都能夠自己用手機更改欲顯示的資訊，利人利己，也讓工作更有效率。
<br>額外小功能：網頁鬧鐘(網頁設定時間，時間到了連接的蜂鳴器會發出聲響提醒，墨水屏也會顯示畫面提示)
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
### 步驟五、安裝FLASK
### 步驟六、製作網頁，並運用FLASK技術作網頁後端伺服器
### 步驟七、將使用者輸入的資料從前端傳到FLASK，再透過墨水屏顯示
### 步驟八、製作網頁鬧鐘，並將時間與樹梅派同步，並讓蜂鳴器與墨水屏同步提示
### 完成上述步驟，即可完成本次專案之功能。
