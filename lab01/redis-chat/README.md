# Key-Value Databases

## 1.5 - Chat System with Redis

​
My first aproach was a direct utilization of the Publish/Susbcribe architecture given by Redis.

However, I came to the conclusion that it was limited and it didn't truly serve all the requirements of the system I wanted to implement.

Thus, I decided to implement my own system (with my own internal architecture).

I decided to use 3 structures to each user:

 1. An **Hash** to store the user information (username, name).
	 
	 The key of the each user's _hash_ is designed in the following way `RedisMS:<username>`. 
	 
	 The actual name of the user is stored in a field called `name`.

	**Example:** `RedisMS:vascoalramos name  "Vasco Ramos"`


2. A **List** to store the messages written by the user.
	
	The key of the each user messages  _list_ is designed in the following way `RedisMessages:<username>`. 

	Every time the user sends a new message, that message is stored in the list using an **lpush** so that the most recent messages appear first.


3. A **Set** to store the subscriptions of the user because a user does not follow the same person twice.
	
	The key of the each user subscriptions  _set_ is designed in the following way `RedisFollowing:<username>`. 


With these 3 structures, I allow the user to send new messages, check existing messages and follow new users.

The system implements the following features:

 - login
 - send new message (publish)
 - check messages from subscriptions
 - check messages sent
 - follow users
 - unfollow users

I will now display an execution example to show the usage of the chat system:


### User 1 (vascoramos)
```
Welcome to Redis Message Server
Insert your username: vascoramos
Insert your name (first and last): Vasco Ramos

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 2
You don't follow anyone (there are no messages).

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 3
You didn't sent any messages!

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 4
----- Users List -----
    ds
    vascoalramos
    vr

User to follow (username): ds

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 4
----- Users List -----
    ds
    vascoalramos
    vr

User to follow (username): vr   

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 5
----- Following ------
  ds
  vr

User to unfollow (username): ds

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 2
-- Messages from User: vr --
  Boas ds!

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 1
Message to send: Olá malta!

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 6
Goodbye! :)
```


### User 2 (diogosilva):
```
Welcome to Redis Message Server
Insert your username: diogosilva
Insert your name (first and last): Diogo Silva

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 4
----- Users List -----
    ds
    vascoramos
    vr
    vascoalramos

User to follow (username): vascoramos

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 4
----- Users List -----
    ds
    vascoramos
    vr
    vascoalramos

User to follow (username): vr

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 4
----- Users List -----
    ds
    vascoramos
    vr
    vascoalramos

User to follow (username): ds

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 4
----- Users List -----
    ds
    vascoramos
    vr
    vascoalramos

User to follow (username): vr

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 2
-- Messages from User: vr --
  Boas ds!
-- Messages from User: vascoramos --
  Olá malta!
-- Messages from User: ds --

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 1
Message to send: Olá Pessoal!

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 3
--- Messages You Sent ---
  Olá Pessoal!

1) Send message
2) Check messages from subscriptions
3) Check messages sent
4) Follow users
5) Unfollow users
6) Exit
>>> 6
Goodbye! :)
```
