import redis

# create the redis connection
r = redis.Redis()

class Person():
    def __init__(self, username, name):
        self.username = username
        self.name = name
    
    def __str__(self):
        return self.username

def main():
    print("Welcome to Redis Message Server")

    username = input("Insert your username: ")
    name = input("Insert your name (first and last): ")
    person = Person(username, name)
    # print(f"({person.username}) {person.name}")

    r.hset(f"RedisMS:{person.username}","name",person.name)

    while True:
        options = "1) Send message\n2) Check messages\n3) Follow users\n4) Exit\n>>> "
        op = input(options)
        if (op == "4"):
            break

        elif (op == "1"):
            message = input("Message to send: ")
            r.lpush(f"RedisMessages:{person.username}", message)

        elif (op == "2"):
            following = r.smembers(f"RedisFollowing:{person.username}")
            if (following is None):
                print("You don't follow anyone (there are no messages).\n")
            
            else:
                for user in following:
                    user = str(user, 'utf-8')
                    print(f"-- Messages from User: {user}")
                    message_list = r.lrange(f"RedisMessages:{user}",0,-1)
                    for msg in message_list:
                        print(f"  {str(msg, 'utf-8')}")

        elif (op == "3"):
            users = r.keys("RedisMS:*")
            print("----- Users List -----")
            users_list = [str(user, "utf-8")[8:] for user in users]
            for user in users_list:
                print(user)
            user_to_follow = input("User to follow (username): ")
            if user_to_follow == person.username:
                print("You can't follow yourself!\n")
            else:
                r.sadd(f"RedisFollowing:{person.username}", user_to_follow)

        else:
            print("Input error!\n")


if __name__ == "__main__":
    main()