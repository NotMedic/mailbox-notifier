#import esp32
from config import *
from machine import Pin, ADC, SoftSPI, I2C, Timer
from sx127x import SX127x
from ssd1306 import SSD1306_I2C
from time import time, sleep, sleep_ms
from json import loads,dumps

try:
    # Initialize LoRa module
    device_spi = SoftSPI(baudrate = 10000000, 
                        polarity = 0,
                        phase = 0,
                        bits = 8,
                        firstbit = SoftSPI.MSB,
                        sck = Pin(lora_spi_config['sck'], Pin.OUT, Pin.PULL_DOWN),
                        mosi = Pin(lora_spi_config['mosi'], Pin.OUT, Pin.PULL_UP),
                        miso = Pin(lora_spi_config['miso'], Pin.IN, Pin.PULL_UP)
                        )

    lora = SX127x(device_spi,
                pins=lora_spi_config)

    i2c = I2C(scl=Pin(oled_i2c_config['scl'], Pin.OUT, Pin.PULL_UP),
            sda=Pin(oled_i2c_config['sda'], Pin.OUT, Pin.PULL_UP)
            )

    i2c_rst = Pin(16, Pin.OUT)
    # Initialize the OLED display
    i2c_rst.value(0)
    sleep_ms(5)
    i2c_rst.value(1) 

    oled = SSD1306_I2C(oled_parameters['width'], oled_parameters['height'], i2c)

    #Set up our Notification LED
    led = Pin(12, Pin.OUT)
    led.value(1)

    ## The Debounce to keep the interrupt from triggering multiple times
    debounce_timer = Timer(-1)


    def debounce_handler(pin):
        # global message_time, message_waiting
        print("Interrupt triggered, turning off LED")
        led.value(1)
        oled.invert(0)
        oled.fill(0)
        oled.text("Listening...", 0, 0)
        oled.show()

    def handle_interrupt(pin):
        global debounce_timer, notification_count
        debounce_timer.init(period=200, mode=Timer.ONE_SHOT, 
            callback=lambda t:debounce_handler(pin))
        notification_count = 0
        
    #Set up our LED Reset Button and Debounce
    ## The Pin
    pin36 = Pin(36, Pin.IN)
    pin36.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

    notification_count = 0

    oled.fill(0)
    oled.text("Listening...", 0, 0)
    oled.show()

    #Sit in a Tight Loop and Wait for a Message
    while True:
        if lora.received_packet():
            recieved_packet = lora.read_payload()
            payload_str = recieved_packet.decode()
            print('Received: {}'.format(payload_str))
            
            # Parse the JSON string to a dictionary
            payload_dict = loads(payload_str)
            
            if payload_dict['status'] == 'Mail!':
                print('You\'ve got mail!')
                notification_count += 1
                led.value(0)
                oled.fill(0)
                oled.invert(1)
                oled.text("Count: " + str(notification_count), 0, 45)
                oled.text("Voltage: " + str(payload_dict['voltage']) + "v", 0, 55)
                oled.show()
                reply = 'Hello'
                print('Sending Reply: {}'.format(reply))
                lora.println(reply)

except Exception as e:
    import machine
    machine.reset()

import machine
machine.reset()