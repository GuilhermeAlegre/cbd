import redis

# create the redis connection
r = redis.Redis()

# drop all data
r.flushdb()

with open("nomes-registados-2018.csv", "r") as reader:
    for line in reader:
        line_array = line.strip().split(",")
        r.zadd("names_distribution", {line_array[0]: line_array[2]})