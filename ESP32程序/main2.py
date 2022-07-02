# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()# 整体流程
# 1. 链接wifi
# 2. 读取服务器数据
# 3. 判断flag
# 4. 处理接收的数据


import socket
import time
import network
import machine
import urequests
import json
import dht

wlan = network.WLAN(network.STA_IF)

def do_connect():
    global wlan
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('HQ', '@LHQ200088')
        i = 1
        while not wlan.isconnected():
            pass
        
    print('network config:', wlan.ifconfig())

def main():
    # 1. 链接wifi
    do_connect()
    # 2. 创建灯的对象和温湿度传感器的对象
    led = machine.Pin(2, machine.Pin.OUT)
    # 3. 接收网络数据
    while True:
        try:
            re = urequests.get("http://121.37.109.178:5000/getFlag")
            re_end = json.loads(re.text)
            flag = re_end["flag"]
            print(flag)
            if (flag == 1):
                led.value(1)
            elif (flag == 0):
                led.value(0)
            elif (flag == 2):
                d = dht.DHT11(machine.Pin(4))
                d.measure()
                t = d.temperature()
                h = d.humidity()
                post_data = {'t':t, 'h':h}
                # print(t,h)
                dht11_lts_url = "http://121.37.109.178:5000/getdht11_lts?t="+str(t)+"&h="+str(h)
                # ht_data = urequests.get(url="http://121.37.109.178:5000/getdht11", json=post_data)
                
                ht_data = urequests.get(dht11_lts_url)
                # print(ht_data.text)
            time.sleep(0.01)
        except OSError:
            global wlan
            wlan.active(False)
            do_connect()
            

if __name__ == "__main__":
    main()






