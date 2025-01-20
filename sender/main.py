
from config import *
from machine import Pin, ADC, SoftSPI, I2C
from sx127x import SX127x
from ssd1306 import SSD1306_I2C
from time import time, sleep, sleep_ms
from json import dumps

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

    # Heltec LoRa 32 with OLED Display
    # oled_width = 128
    # oled_height = 64
    # OLED reset pin
    # i2c_rst = Pin(16, Pin.OUT)
    # # Initialize the OLED display
    # i2c_rst.value(0)
    # sleep_ms(5)
    # i2c_rst.value(1) # must be held high after initialization
    # Setup the I2C lines
    # i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
    # i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
    # # Create the bus object
    # i2c = I2C(scl=i2c_scl, sda=i2c_sda)
    # Create the display object
    # oled = SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)

    oled.text('There\'s light!', 0, 0)
    oled.show()

    #oled.line(0, 0, 50, 25, 1)
    oled.show()

    turn_off = Pin(25, Pin.OUT)
    turn_off.value(0)

    #Constants for voltage calculation
    XS = 0.0025
    MUL = 1000
    #Pin 21 must be low to read voltage.
    twentyone = Pin(21, Pin.OUT)
    twentyone.value(0)
    adc_pin = Pin(13, Pin.IN)
    adc = ADC(adc_pin)
    adc.atten(ADC.ATTN_11DB)
    adc.init()

    voltage = round(adc.read_uv() * XS * MUL / 1000000 - 0.3,2)

    oled.text('Voltage: ' + str(voltage), 0, 10)
    oled.show()

    packet_to_send = {'status': 'Mail!',
            'voltage': voltage}

    packet_to_send['voltage'] = voltage

    retry_count = 0

    while True and retry_count < 3:
        oled.text('Sending ', 0, 20)
        oled.show()
        lora.println(dumps(packet_to_send))
        start_time = time()
        timeout = 30  # seconds
        while not lora.received_packet():
            if time() - start_time > timeout:
                print("Timeout: No packet received within 30 seconds, sending again")
                break
        
        packet = lora.read_payload().decode()
        if packet == 'Hello':
            print("ACK")
            oled.text('ACK', 0, 40)
            oled.show()
            print("shutting down")
            oled.text('Shutting Down', 0, 50)
            oled.show()
            turn_off.value(1)
            sleep(1)
            turn_off.value(0)
            break

        retry_count += 1

        oled.text('Retry ' + str(retry_count), 0, 30)

    else:
        print("Didn't recieve a reply")
        print("shutting down")
        turn_off.value(1)
        sleep(1)
        turn_off.value(0)

    print("I should not be here. This means I still have power.")
    print("I think I'll go to sleep now.")
    oled.fill(0)
    oled.text('Charging?', 0, 0)
    oled.text('Power Cycle to', 0, 10)
    oled.text('return to normal', 0, 20)
    oled.show()

except Exception as e:
    import machine
    machine.reset()