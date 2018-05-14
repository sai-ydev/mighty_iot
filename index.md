## Citizen Science With MicroPython
Thanks for signing up for the workshop. We are DIY enthusiasts and big fans of the Micropython world. We put this workshop together to share our knowledge with others. This workshop is by no means a comprehensive guide to Micropython but the contents in the workshop should get you started with collecting simple data points using MicroPython. 

The workshop materials are written using the [MicroPython Documentation for ESP8266](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html). Some of the code snippets used in the workshop were actually used directly 

# Documentation

The official documentation for running the MicroPython on the ESP8266 is available from [here](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html). The documentation goes into much more detail than the workshop's documentation. 

# Firmware Download

The ESP8266 in the kit comes with the firmware installed on the hardware. For future firmware updates, the latest build of Micropython is available from [here](http://micropython.org/download#esp8266).  (Todo: Tutorial on installing the firmware)

# Workshop kit contents

Your workshop kit contains the following components:

1. WeMoS ESP8266 development board
2. DHT11 Temperature Humidity Sensor 
3. GUVA-S12SD Analog UV Sensor
4. CCS811 sensor 
5. Jumper Wires, Resistors
6. Breadboard

# Requisite Tool Installation on your laptop

1. The first step is installation of the esptool on your laptop. The esptool is available from the Python package manager. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* The first step is to install Python on your laptop (3.x) (You can skip this step if you have installed Python on your laptop).
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Then, esptool can be installed as follows: 

```
pip install esptool
```
# Setting up WiFi credentials

The WiFi on your ESP8266 is already setup for the workshop. 


# Introduction Tutorial - Hello World

In order to test whether things are properly setup, let's perform a basic exercise of blinking an LED using the ESP8266. For this exercise, we will need the following items (provided in the kit): 
1. ESP8266 Development Board 
2. 1 x LED
3. 220 ohm resistor

Connect the LED to the 220 ohm resistor as shown in the figure below: 

![Image](https://github.com/sai-y/circuitpython_workshop/blob/master/images/LED_Blinking_bb.png)

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
led.on()
```

If the LED turns on, we can turn it off as:

```
led.off()
```
If your LED doesn't turn on, check the connections (especially, the LED polarity). Now that we have tested the LED, let's make it blink at a 1 second interval: 
```

```
# Publishing data to the internet 

# Interfacing the Temperature/Humidity sensor


# Interfacing the UV sensor



# Interfacing the VOC sensor

# Further Resources

Online 