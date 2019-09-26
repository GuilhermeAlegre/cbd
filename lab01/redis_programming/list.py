import redis

# create the redis connection
r = redis.Redis()

# drop all data
r.flushdb()

users = ["Vasco", "Diogo", "João", "Tomás"]

# insert in list named users_list
for user in users:
    r.lpush("users_list", user.encode("utf-8"))

# get the list "users_list"
members = r.lrange("users_list", 0, -1)

# print the list decoded to utf-8
print([str(name, "utf-8") for name in members])