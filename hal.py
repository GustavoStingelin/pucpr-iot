import random
from enum import Enum


class HeaterState(Enum):
    on = 1
    off = 0


def get_temperature():
    return random.randrange(2, 27)


def get_humidity():
    return random.randrange(40, 95)


def set_heater(state: HeaterState):
    match state:
        case state.on:
            print('Aquecedor LIGADO')
        case state.off:
            print('Aquecedor DESLIGADO')
