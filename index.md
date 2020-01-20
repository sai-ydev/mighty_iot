# Mighty IoT With MicroPython
Thanks for signing up for the workshop. We are DIY enthusiasts and big fans of Micropython.

The workshop materials are written using the [MicroPython Documentation for ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html).

# MicroPython vs CircuitPython


MicroPython and CircuitPython are similar and the latter was spun off the former.

# Documentation

The official documentation for running the MicroPython on the ESP8266 is available from [here](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html). The documentation goes into much more detail than the workshop's documentation.

# Firmware Download

The ESP32 in the kit comes with the firmware installed on the hardware. For future firmware updates, the latest build of Micropython is available from [here](http://micropython.org/download#esp32).  (Todo: Tutorial on installing the firmware)

# Workshop kit contents

Your workshop kit contains the following components:

1. [ESP32 Development Board](https://www.amazon.com/dp/B07Q576VWZ/ref=cm_sw_r_tw_dp_U_x_uHpjEbEAC3P26)
2. [AM2320 Digital Temperature and Humidity Sensor](https://www.adafruit.com/product/3721)
3. [VEML6070 UV Index Sensor Breakout](https://www.adafruit.com/product/2899)
4. [1 x Neopixel in breadboard form factor](https://www.adafruit.com/product/1312)
5. [1 x Tactile Button](https://www.sparkfun.com/products/10442)
6. [1 x Trim Potentiometer]()
7. [1 x Red Led](https://www.digikey.com/product-detail/en/kingbright/WP7113LSRD/754-1267-ND/1747666)
8. Jumper Wires
9. Resistors (330 ohms x 1, 4.7K x 2, 10K x 1)
10. Breadboard

# Software setup

You can just your text editor. For the sake of convenience, we will be using the [Thonny IDE](thonny.org). It is available for Windows, MAC and Linux Operating Systems. Once you have installed Thonny, launch the IDE and configure it for ESP32 on MicroPython as follows:

1. Go to Run --> Select Interpreter:
![]({{"/images/thonny_select_interpreter.png"|absolute_url}})
2. Set the interpreter to Micropython (ESP32) and the port to your ESP32's serial port (shown in the snapshot below). If you have a Windows machine and no serial ports were detected, you might have to install its drivers.
![]({{"/images/thonny_serial_port.png"|absolute_url}})

# ESP32 Pinout

The board used for the workshop is the WeMos ESP8266 development board. The image below describes the pinout of the WeMos ESP8266 development. It describes the function of each pin:

![]({{"/images/ESP32-pinout-mapping.png"|absolute_url}})

# Introduction Tutorial - Hello World

In order to test whether things are properly setup, let's perform a basic exercise of blinking an LED using the ESP8266. For this exercise, we will need the following items (provided in the kit):
1. ESP8266 Development Board
2. 1 x LED
3. 220 ohm resistor

Connect the LED to the 220 ohm resistor as shown in the figure below:

![]({{"/images/LED_Blinking_bb.png"|absolute_url}})

Upon completing the connections, the first step is to test whether the LED has been connected properly. In order to test the connection, import the `machine` module. The `machine` module provides access to the GPIO pins on the ESP8266.

```
>>> import machine
```

The next step is to initialize a GPIO pin. Since we connected our LED to the GPIO Pin 0:

```
>>> led = machine.Pin(0, machine.Pin.OUT)
```

Now, let's determine whether the LED turns on:

```
>>> led.on()
```

If the LED turns on, we can turn it off as:

```
>>> led.off()
```
If your LED doesn't turn on, check the connections (especially, the LED polarity). Now that we have tested the LED, let's make it blink at a 1 second interval:
```
import machine
import time

led = machine.Pin(0, machine.Pin.OUT)

def blink():
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
```

In the above example, we are making the LED blink at a 1 second interval. In order to introduce a delay, we are using the `time` module. We are using the `sleep()` to introduce a delay in our program. The `sleep()` method requires an integer as an argument.

Let's save the file (as led.py) and send it to the ESP8266 (via the WebREPL or ampy). Once the file is uploaded, it could be executed as follows:

```
import led
led.blink()
```

Now that we have completed the basic example, let's move on to the next section!

# Interfacing the UV sensor

In this section, we will learn to the interface the GUVA-S12SD Analog UV Sensor. The ESP8266 has 1 analog input and we will be interfacing the UV sensor to this analog input.

```
>>> import machine
>>> adc = machine.ADC(0)
>>> adc.read()
```

Now, let's find out if there is a fluctuation in UV index levels using a **UV torch light** (Insert link to UV Torch Light):

```
while True:
    print(adc.read() * (3.3/102.4))
```

### Note:
UV Torchlights can be harmful to the eyes. Care should be taken while handling a UV torch light. Do not make direct eye contact with the Uv torch light.

# Publishing data to the internet

In this tutorial, we will learn to save the UV index levels to a spreadsheet. The first step is to get the IFTTT webhook and key (To do: Tutorial on setting up a webhook).

The UV sensor needs to be interfaced to the ESP8266 as shown in the figure below:

![]({{"/images/UV_Sensor_Sketch_bb.png"|absolute_url}})

We can trigger the webhook as follows:

```
import machine
import ifttt
import time

adc = machine.ADC(0)
KEY = IFTTT_KEY
EVENT = voc2_data


def publish_values():
    value1 = (adc.read() * 3.3)/102.4
    ifttt.post(EVENT, KEY, value1=value1)

```

### `ifttt` module

The ifttt module used in the above code snippet is a wrapper around the `POST` request used to trigger the webhook. The ifttt wrapper is available from **here** (Insert Link).

# Interfacing the Temperature/Humidity sensor

In this section, we will interface a DHT11 sensor to the ESP8266 and we will be using the [dht driver module](https://github.com/micropython/micropython/tree/master/drivers/dht). In the previous example, we uploaded to the spreadsheet only when the function `publish_values` is called. In this tutorial, we will review writing scripts that uploads to the cloud at regular interval.

The DHT11 sensor needs to be interfaced to the ESP8266 as shown in the figure below:

![]({{"/images/DHT11_bb.png"|absolute_url}})

Once the DHT drivers are uploaded to the ESP8266 module, the temperature and relative humidity can be measured as follows:

```
>>> import dht
>>> import machine
>>> d = dht.DHT11(machine.Pin(4))

>>> d.measure()
>>> d.temperature()
>>> d.humidity()
```

If there are problems reading the temperature from the sensor, check your connections and ensure that there is a pull-up resistor on the data pin.

According to the micropython documentation, the script `main.py` is executed right after the board finishes booting up. So, let's write a script that publishes the temperature and relative humidity value to a Google spreadsheet every 30 seconds.  
```
import dht
import machine
import ifttt
import time

d = dht.DHT11(machine.Pin(4))

while True:
    d.measure()
    response = ifttt.post(EVENT_NAME, KEY, value1=d.temperature(), value2=d.humidity())
    time.sleep(30)
```

The script needs to be uploaded to the ESP8266 using [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/boot-scripts) (You have to install ampy on your laptop):

```
ampy --port COM11 put dht_test.py /main.py
```
# Interfacing the VOC sensor

The CCS811 is an indoor air quality sensor that measures the total volatile organic compounds (TVOC) and provides equivalent carbon dioxide levels. The CCS811 sensor can be interfaced to the ESP8266 as shown in the figure below:

![]({{"/images/ccs811_bb.png"|absolute_url}})

Let's put the sensor to test:

```
from ccs811 import CCS811
from machine import Pin, I2C
import time

def main():  
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    s = CCS811(i2c)
    time.sleep(1)
    while True:
        if s.data_ready():
            print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
            time.sleep(1)
```

The sensor output should look something like shown below:

![]({{"/images/ccs811_screenshot.png"|absolute_url}})

## Challenge

Try uploading the VOC sensor data to the cloud

# Online PyBoard

[Micropython PyBoard](http://micropython.org/live/)

# Further Resources
# Requisite Tool Installation on your laptop

1. The first step is installation of the esptool on your laptop. The esptool is available from the Python package manager.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* The first step is to install Python on your laptop (3.x) (You can skip this step if you have installed Python on your laptop).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Then, esptool can be installed as follows:

```
pip install esptool
```
# Setting up WiFi credentials

The WiFi credentials on your ESP8266 is already setup for the workshop. But this is how you set it up:

```
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ssid', 'password')
```
