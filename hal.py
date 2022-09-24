import random
from enum import Enum

from definitions import expected_temp


class HeaterState(Enum):
    on = 1
    off = 0


def get_temperature(heater_state: HeaterState, last_temp: int):
    if last_temp is None:
        return expected_temp - 5
    elif heater_state == HeaterState.on:
        return last_temp + (random.randrange(9, 25) / 10)
    else:
        return last_temp - (random.randrange(9, 25) / 10)


def set_heater(state: HeaterState):
    match state:
        case state.on:
            print('Aquecedor LIGADO')
        case state.off:
            print('Aquecedor DESLIGADO')
