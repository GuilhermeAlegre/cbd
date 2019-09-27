import redis

# create the redis connection
r = redis.Redis()

# input text to user
txt = input("Search for ('Enter for quit): ")

if (txt != ""):
    # execute redis command "keys <txt>*"
    for user in sorted(r.keys(f"{txt}*")):
        print(str(user, "utf-8"))
else:
    print("See u next time! ;)")