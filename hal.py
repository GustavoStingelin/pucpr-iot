import random
from enum import Enum


class HeaterState(Enum):
    on = 1
    off = 0


def get_temperature():
    return random.randrange(20, 40, 10)


def set_heater(state: HeaterState):
    match state:
        case state.on:
            print('Aquecedor LIGADO')
        case state.off:
            print('Aquecedor DESLIGADO')
