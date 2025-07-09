import redis
import json

class RedisManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()

    def redis_subscriber(self, *channels, callback=None):
        try:
            if not channels:
                raise ValueError("At least one channel must be provided")

            self.pubsub.subscribe(*channels)
            print(f"Subscribed to channels: {', '.join(channels)}")

            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        key = data.get('key')
                        value = data.get('value')

                        print(f"Received on {message['channel']}:")
                        print(f"   Key    : {key}")
                        print(f"   Value  : {value}")

                        if callback:
                            callback(key, value)

                    except json.JSONDecodeError:
                        print("Received non-JSON message:", message['data'])
            
        except Exception as e:
            print(f"Error subscribing to {', '.join(channels)}: {e}")

    def redis_publisher(self, channel, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)

            self.redis_client.publish(channel, message)
            print(f"Published to '{channel}': {message}")

        except Exception as e:
            print(f"Error publishing to {channel}: {e}")
