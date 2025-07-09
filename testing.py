from RedisManager import RedisManager
import threading
import time

client = RedisManager()

def pub_to_channel():
    client.redis_publisher("some_channel", {"key": "test key", "value": "test value"})

def some_callback(key, value):
    print(f"Callback! for key: {key} and value: {value}")

def sub_to_channel():
    client.redis_subscriber("some_channel", callback=some_callback)

if __name__ == '__main__':
    threading.Thread(target=sub_to_channel, daemon=True).start()

    while True:
        time.sleep(0.1)
        input("Send a pub test:")
        pub_to_channel()
