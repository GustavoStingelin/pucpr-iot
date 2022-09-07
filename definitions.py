import os

server = 'mqtt.mydevices.com'
port = 1883

user = os.getenv('user')
password = os.getenv('password')
client_id = os.getenv('client_id')

def topic_data(channel: str): return f"""v1/{user}/things/{client_id}/data/{channel}"""
def topic_cmd(channel: str): return f"""v1/{user}/things/{client_id}/cmd/{channel}"""
def topic_response(): return f"""v1/{user}/things/{client_id}/response"""


temperature_topic_data = topic_data(0)
humidity_topic_data = topic_data(1)
heater_topic_cmd = topic_cmd(2)
heater_topic_response = topic_response()
