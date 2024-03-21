from Adafruit_IO import MQTTClient
import random
import sys
import time


class MyMQTTClient(MQTTClient):
    def __init__(self, username, key, config):
        super().__init__(username, key)
        self.config = config
        self.on_connect = self.my_connect
        self.on_disconnect = self.my_disconnect
        self.on_message = self.my_message
        self.on_subscribe = self.my_subscribe
        self.on_unsubscribe = self.my_unsubscribe
        self.on_publish = self.my_publish
        self.on_publish_multiple = self.my_publish_multiple
        self.on_sample = self.my_sample
        self.connect()
        self.loop_background()

    def my_connect(self, client):
        print('Connected to Adafruit IO!  Listening for {0} changes...'.format(self.config['aio_feed_id']))
        try:
            print(self.config['aio_feed_id'])
            print(type(self.config['aio_feed_id']))
            for feed in self.config['aio_feed_id']:
                client.subscribe(feed)
        except:
            print("Error: ", sys.exc_info()[0])
    
    def my_disconnect(self, client):
        print('Disconnected from Adafruit IO!')
        sys.exit(1)

    def my_message(self, client, feed_id, payload):
        print('Feed {0} received new value: {1}'.format(feed_id, payload))

    def my_subscribe(self, client, user_data, mid, granted_qos):
        print('Subscribed to {0} with QoS {1}'.format(mid, granted_qos))

    def my_unsubscribe(self, client, user_data, mid):
        print('Unsubscribed from {0}'.format(mid))
        self.unsubscribe(self.config['aio_feed_id'])
        self.disconnect()

    def my_publish(self, client, feed_id, payload, retain, qos):
        print('Published to {0} with QoS {1}'.format(feed_id, qos))
        self.publish(feed_id, payload, retain, qos)

    def my_publish_multiple(self, client, tuple_list, qos, retain):
        print('Published multiple values with QoS {0}'.format(qos))

    def my_sample(self, client):
        print('Publishing a sample of values...')
        counter = 1000
        while True:
            if counter > 0:
                temp = random.randint(10, 100)
                client.publish(self.config['aio_feed_id'][0], temp)
                humidity = random.randint(50, 90)
                client.publish(self.config['aio_feed_id'][1], humidity)
                sound = random.randint(0, 100)
                client.publish(self.config['aio_feed_id'][2], sound)
                battery = random.randint(0, 100)
                client.publish(self.config['aio_feed_id'][3], battery)
                counter -= 1
                time.sleep(5)
            else:
                client.disconnect()
                break
