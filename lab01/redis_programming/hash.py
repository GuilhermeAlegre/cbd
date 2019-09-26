import redis

# create the redis connection
r = redis.Redis()

# drop all data
r.flushdb()

users = [("Vasco", 20), ("Diogo", 19), ("João", 18), ("Tomás", 15)]

# insert in list named users_hash
for idx, user in enumerate(users):
    r.hmset(f"USERS:{idx}", {"name": user[0], "age": user[1]})

# get the hash of each user
for idx, user in enumerate(users):
    print(dict((str(key, "utf-8"), str(value, "utf-8"))
               for key, value in r.hgetall(f"USERS:{idx}").items()))
