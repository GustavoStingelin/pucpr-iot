import os

server = 'mqtt.mydevices.com'
port = 1883

user = os.getenv('user')
password = os.getenv('password')
client_id = os.getenv('client_id')


def topic_data(channel: str): return f"""v1/{user}/things/{client_id}/data/{channel}"""


temperature_topic_data = topic_data(0)
heater_state_topic_data = topic_data(3)
temperature_control_topic_cmd = f"""v1/{user}/things/{client_id}/cmd/2"""
topic_response = f"""v1/{user}/things/{client_id}/response"""
