##Grabbing functions for humidity

import Adafruit_DHT as dht

def grab_sensors_hum(GPIO_pin=22):
    h,t = dht.read_retry(dht.DHT22, GPIO_pin)
    hum = "{0:0.2f}".format(h)
    return {'dht22':hum}
