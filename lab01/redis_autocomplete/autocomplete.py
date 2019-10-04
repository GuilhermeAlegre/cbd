import redis
import re

# create the redis connection
r = redis.Redis()

# input text to user
txt = input("Search for ('Enter for quit): ")

if (txt != ""):
    # execute redis command "zrange names_distribution 0 1"
    keys = r.zrange("names", start=0, end=-1)

    # filter all words in sorted set for the ones which start with the input value
    keys = [str(key, 'utf-8').strip() for key in keys if re.search(f"^{txt}", str(key, 'utf-8'))]

    for key in keys:
        print(key)
else:
    print("See u next time! ;)")