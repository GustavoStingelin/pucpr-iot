import time
from enum import Enum

import paho.mqtt.client as mqtt

from definitions import client_id, user, password, port, server, temperature_topic_data, \
    temperature_control_topic_cmd, topic_response, heater_state_topic_data
from hal import get_temperature, set_heater, HeaterState


class TemperatureControlState(Enum):
    on = 1
    off = 0


def set_heater_state():
    global temperature_control_state
    if temperature_control_state == TemperatureControlState.on:
        if get_temperature() < 30:
            set_heater(HeaterState.on)
        else:
            set_heater(HeaterState.off)
    else:
        set_heater(HeaterState.off)


def handle_heater_message(message):
    global temperature_control_state
    msg = message.payload.decode().split(',')
    match msg[1]:
        case '1':
            temperature_control_state = TemperatureControlState.on
            print("controle de temperatura LIGADO")
            set_heater_state()
            client.publish(topic_response, msg[0])
        case '0':
            temperature_control_state = TemperatureControlState.off
            print("controle de temperatura DESLIGADO")
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

    while True:
        client.publish(temperature_topic_data, get_temperature())
        client.publish(heater_state_topic_data, heater_state.value)
        print("t: " + str(get_temperature()))
        print("tcs: " + str(temperature_control_state.value))
        print("hs: " + str(heater_state.value))
        time.sleep(10)

    # client.disconnect()
