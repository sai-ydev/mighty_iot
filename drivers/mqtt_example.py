from time import sleep
from machine import Pin, I2C
from umqtt.simple import MQTTClient
import veml6070

i2c = I2C(scl=Pin(5), sda=Pin(4))
uv = veml6070.VEML6070(i2c)

SERVER = "mqtt.thingspeak.com"
client = MQTTClient("umqtt_client", SERVER)

CHANNEL_ID = "ID"
API_KEY = "KEY"

topic = "channels/" + CHANNEL_ID + "/publish/" + API_KEY

while True:
    uv_raw = uv.uv_raw
    risk_level = uv.get_index(uv_raw)
    print('Reading: ', uv_raw, ' | Risk Level: ', risk_level)
    
    payload = "field1=" + risk_level
    client.connect()
    client.publish(topic, payload)
    client.disconnect()
    sleep(10)
