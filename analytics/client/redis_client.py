import redis


def connect():
    r = redis.Redis(host="localhost", port=6379, db=0)
    if not r.ping():
        print("Can't connect to Redis server")
        exit()
    return r


def set_value(r, stream_name, value):
    try:
        value = dict(value)
    except TypeError:
        print("TypeError")
        exit()
    r.xadd(stream_name, value)


r = connect()
set_value(r, "sensor_data", {"temperature": 23.5, "humidity": 45.2})
