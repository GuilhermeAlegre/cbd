import redis

# create the redis connection
r = redis.Redis()

# drop all data
r.flushdb()

with open("female-names.txt", "r") as reader:
    for line in reader:
        r.zadd("names", {line: 0})