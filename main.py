import time
from enum import Enum

import paho.mqtt.client as mqtt

from definitions import client_id, user, password, port, server, temperature_topic_data, \
    temperature_control_topic_cmd, topic_response, expected_temp
from hal import get_temperature, set_heater, HeaterState


class TemperatureControlState(Enum):
    on = 1
    off = 0


def set_heater_state():
    global temperature_control_state, heater_state
    if temperature_control_state == TemperatureControlState.on:
        if expected_temp > last_temp:
            heater_state = HeaterState.on
            set_heater(heater_state)
        else:
            heater_state = HeaterState.off
            set_heater(heater_state)
    else:
        heater_state = HeaterState.off
        set_heater(heater_state)


def handle_heater_message(message):
    global temperature_control_state
    msg = message.payload.decode().split(',')
    match msg[1]:
        case '1':
            print("ligando controle de temperatura")
            temperature_control_state = TemperatureControlState.on
            set_heater_state()
            client.publish(topic_response, msg[0])
        case '0':
            print("desligando controle de temperatura")
            temperature_control_state = TemperatureControlState.off
            set_heater_state()
            client.publish(topic_response, msg[0])


def message_handler(client, user, message):
    match message.topic:
        case temperature_control_topic_cmd: handle_heater_message(message)


if __name__ == '__main__':
    client = mqtt.Client(client_id)
    client.username_pw_set(user, password)
    client.connect(server, port)

    client.on_message = message_handler
    client.subscribe(temperature_control_topic_cmd)
    client.loop_start()

    heater_state = HeaterState.off
    temperature_control_state = TemperatureControlState.off
    last_temp: int = None

    while True:
        last_temp = get_temperature(heater_state, last_temp)
        print("temperatura: %.2fºC" % last_temp)
        client.publish(temperature_topic_data, last_temp, 0)
        time.sleep(0.3)
        set_heater_state()
        time.sleep(5)

    #client.disconnect()
