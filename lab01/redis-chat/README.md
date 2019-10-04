# Key-Value Databases

## 1.5 - Chat System with Redis

​
My first aproach was a direct utilization of the Publish/Susbcribe architecture given by Redis.

However, I came to the conclusion that it was limited and it didn't truly serve all the requirements of the system I wanted to implement.

Thus, I decided to implement my own system (with my own internal architecture).

I decided to use 3 structures to each user:

 1. An **Hash** to store the user information (username, name).

    The key of the each user's hash is designed in the following way `RedisMS:<username>`. 

    The actual name of the user is stored in a field called `name`.
2. A **List** to store the messages written by the user
3. A second **List** to store the subscriptions of the user.
