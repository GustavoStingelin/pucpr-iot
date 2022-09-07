import time

import paho.mqtt.client as mqtt

from definitions import client_id, user, password, port, server
from hal import get_humidity, get_temperature, set_heater, HeaterState


def message_handler(client, user, message):
    topic = message.topic
    match topic:
        case 'pucpr/iotmc/gu/heater':
            msg = message.payload.decode()
            match msg:
                case 'on': set_heater(HeaterState.on)
                case 'off': set_heater(HeaterState.off)


if __name__ == '__main__':
    client = mqtt.Client(client_id)
    client.username_pw_set(user, password)
    client.connect(server, port)

    client.on_message = message_handler
    client.subscribe('pucpr/iotmc/gu/heater')
    client.loop_start()

while True:
    client.publish('pucpr/iotmc/gu/temp', get_temperature())
    client.publish('pucpr/iotmc/gu/hum', get_humidity())
    time.sleep(1)

# client.disconnect()
