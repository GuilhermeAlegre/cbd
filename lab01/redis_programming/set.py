import redis

# create the redis connection
r = redis.Redis()

# drop all data
r.flushdb()

users = ["Vasco", "Diogo", "João", "Tomás"]

# insert in set named users
for user in users:
    r.sadd("users", user.encode("utf-8"))

# get the set "users"
members = r.smembers("users")

# print the set decoded to utf-8
print(set(str(name, "utf-8") for name in members))