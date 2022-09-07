import time

import paho.mqtt.client as mqtt

from definitions import client_id, user, password, port, server, temperature_topic_data, humidity_topic_data, \
    heater_topic_cmd, heater_topic_response
from hal import get_humidity, get_temperature, set_heater, HeaterState


def handle_heater_message(client, user, message):
    msg = message.payload.decode().split(',')
    match msg[1]:
        case '1':
            set_heater(HeaterState.on)
            client.publish(heater_topic_response, msg[0])
        case '0':
            set_heater(HeaterState.off)
            client.publish(heater_topic_response, msg[0])


def message_handler(client, user, message):
    match message.topic:
        case heater_topic_cmd: handle_heater_message(client, user, message)


if __name__ == '__main__':
    client = mqtt.Client(client_id)
    client.username_pw_set(user, password)
    client.connect(server, port)

    client.on_message = message_handler
    client.subscribe(heater_topic_cmd)
    client.loop_start()

while True:
    client.publish(temperature_topic_data, get_temperature())
    client.publish(humidity_topic_data, get_humidity())
    time.sleep(10)

# client.disconnect()
