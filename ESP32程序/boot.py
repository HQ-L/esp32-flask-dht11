# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
# 整体流程
# 1. 链接wifi
# 2. 读取服务器数据
# 3. 判断flag
# 4. 处理接收的数据

# 导入模块
import socket
import time
import network
import machine
import urequests
import json
import dht

# 创建wlan对象
wlan = network.WLAN(network.STA_IF)

# 进行WiFi连接函数，官方文档有参考
def do_connect():
    global wlan
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ChinaNet-aKgz', 'fescqs6m')
        i = 1
        while not wlan.isconnected():
            pass
        
    print('network config:', wlan.ifconfig())

def main():
    # 1. 链接wifi
    do_connect()
    # 2. 创建灯的对象和温湿度传感器的对象，管脚为D12
    led = machine.Pin(12, machine.Pin.OUT)
    # 3. 接收网络数据
    while True:
        try:
            re = urequests.get("http://121.37.109.178:5000/getFlag")
            re_end = json.loads(re.text)
            flag = re_end["flag"]
            print(flag)
            if (flag == 1 or flag == "1"):
                led.value(1)
            elif (flag == 0 or flag == "0"):
                led.value(0)
            elif (flag == 2 or flag == "2"):
                # 创建温湿度传感器的对象，data管脚为D4
                d = dht.DHT11(machine.Pin(4))
                d.measure()
                t = d.temperature()
                h = d.humidity()
                # 往服务器传的值
                post_data = {'t':t, 'h':h}
                # print(t,h)
                # dht11_lts_url = "http://121.37.109.178:5000/getdht11_lts?t="+str(t)+"&h="+str(h)
                # POST请求为传值
                ht_data = urequests.post(url="http://121.37.109.178:5000/getdht11", json=post_data)
                # 设置flag的值使flag=2只传一次防止esp32模块崩溃
                re1 = urequests.get("http://121.37.109.178:5000/setFlag?flag=0")
                # led灯闪烁一下代表获取温湿度数据结束
                led.value(0)
                time.sleep(0.5)
                led.value(1)
                time.sleep(0.5)
                
                # ht_data = urequests.get(dht11_lts_url)
                # print(ht_data.text)
            time.sleep(0.01)
        # 防止ESP32宕机，重新连接
        except OSError:
            global wlan
            wlan.active(False)
            do_connect()
            
# 程序入口
if __name__ == "__main__":
    main()







