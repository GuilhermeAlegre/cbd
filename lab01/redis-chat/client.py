import redis

# create the redis connection
r = redis.Redis()


# class representative of the system's users
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

    r.hset(f"RedisMS:{person.username}", "name", person.name)

    while True:
        options = "\n1) Send message\n2) Check messages from subscriptions\n3) Check messages sent\n4) Follow users\n5) Unfollow users\n6) Exit\n>>> "
        op = input(options)

        if (op == "6"):
            print("Goodbye! :)")
            break

        elif (op == "1"):
            message = input("Message to send: ")
            r.lpush(f"RedisMessages:{person.username}", message)

        elif (op == "2"):
            following = r.smembers(f"RedisFollowing:{person.username}")
            if (following == set()):
                print("You don't follow anyone (there are no messages).")

            else:
                for user in following:
                    user = str(user, 'utf-8')
                    print(f"-- Messages from User: {user} --")
                    message_list = r.lrange(f"RedisMessages:{user}", 0, -1)
                    for msg in message_list:
                        print(f"  {str(msg, 'utf-8')}")

        elif (op == "3"):
            messages_sent = r.lrange(f"RedisMessages:{person.username}", 0, -1)
            if (messages_sent == []):
                print("You didn't sent any messages!")
            else:
                print(f"--- Messages You Sent ---")
                for msg in messages_sent:
                    print(f"  {str(msg, 'utf-8')}")

        elif (op == "4"):
            users = r.keys("RedisMS:*")
            print("----- Users List -----")

            users_list = [str(user, "utf-8")[8:] for user in users]
            users_list.remove(person.username)
            for user in users_list:
                print(f"    {user}")

            user_to_follow = input("\nUser to follow (username): ")

            if (user_to_follow == person.username):
                print("You can't follow yourself!")
            elif (user_to_follow not in users_list):
                print("The specified user does not exist!")
            else:
                r.sadd(f"RedisFollowing:{person.username}", user_to_follow)

        elif (op == "5"):
            following = [str(user, 'utf-8')
                         for user in r.smembers(f"RedisFollowing:{person.username}")]

            if (following == []):
                print("You don't follow anyone.")
            else:
                print("----- Following ------")
                for user in following:
                    print(f"  {user}")

                user_to_unfollow = input("\nUser to unfollow (username): ")
                if user_to_unfollow not in following:
                    print("You don't follow the specified user!")
                r.srem(f"RedisFollowing:{person.username}", user_to_unfollow)

        else:
            print("Input error! Please try again.")


if __name__ == "__main__":
    main()
