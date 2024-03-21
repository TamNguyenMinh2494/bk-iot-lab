import json 
from mqtt_client import MyMQTTClient

def load_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
    return config


if __name__ == '__main__':
    config = load_config()
    client = MyMQTTClient(config['aio_username'], config['aio_key'], config=config)
    client.my_sample(client)




   
