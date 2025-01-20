lora_spi_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'dio_1':35,
    'dio_2':34,    
    'reset':14,
    'led':25,
}

lora_parameters = {
    'frequency': 903E6, 
    'tx_power_level': 20, 
    'signal_bandwidth': 62.5E3,    
    'spreading_factor': 12, 
    'coding_rate': 8, 
    'preamble_length': 12,
    'implicit_header': False, 
    'sync_word': 0x12, 
    'enable_CRC': False,
    'invert_IQ': False,
}

oled_i2c_config = {
    'sda': 4,
    'scl': 15,
    'rst': 16,
}

oled_parameters = {
    'width': 128,
    'height': 64,
}