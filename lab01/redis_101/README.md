# Redis Cheat Sheet


## Keys
Redis `keys` are binary safe (any binary stream can be used as a key) although the most common (and recommended) stream to use is a string key, like "Person", other file formats and binary streams like images, mp3, or other file formats, can be used.

### EXISTS key
Returns **1** if the specified key exists. Returns **0** otherwise.
If passed multiple keys, the return value is the number of keys existing among the ones specified as arguments (keys mentioned multiple times and existing are counted multiple times).
```
redis> SET key1 "Hello"
"OK"
redis> EXISTS key1
(integer) 1
redis> EXISTS nosuchkey
(integer) 0
redis> SET key2 "World"
"OK"
redis> EXISTS key1 key2 nosuchkey
(integer) 2
```

### TYPE key
Returns the string representation of the type of the value stored at `key` (can be returned: `string`, `list`, `set`, `zset`, `hash` and `stream`).
```
redis> SET key1 "value"
"OK"
redis> TYPE key1
"string"
```

### DEL key
Removes the specified keys. A key is ignored if it does not exist.
Returns the number of keys that were removed.
```
redis> SET key1 "Hello"
"OK"
redis> SET key2 "World"
"OK"
redis> DEL key1 key2 key3
(integer) 2
```

#### KEYS pattern
Returns all keys matching `pattern`.
```
redis> SET testkey "hello"
OK
redis> SET secondkey "hello again"
redis> KEYS *
1) "testkey"
2) "secondkey"
```


## String
In Redis, strings are serialized characters in C. Integers are stored in Redis as a string.

### SET key string optional nx|xx
Set `key` to hold the string `value`. If `key` already holds a value, it is overwritten, regardless of its type. Any previous time to live associated with the key is discarded on successful `SET` operation.

**Options:**
-   `EX` _seconds_ -- Set the specified expire time, in seconds.
-   `PX` _milliseconds_ -- Set the specified expire time, in milliseconds.
-   `NX` -- Only set the key if it does not already exist.
-   `XX` -- Only set the key if it already exist.

**Return value:**
- `OK` if SET was executed correctly.
- `(nil)` if the SET operation was not performed because the user specified the `NX` or `XX` option but the condition was not met.
```
redis> SET mykey "Hello"
"OK"
redis> SET mybabkey "Hello again" XX
(nil)
```

### GET key
Get the value of `key`. 
If the key does not exist the special value `nil` is returned. An error is returned if the value stored at `key` is not a string, because GET only handles string values.
```
redis> GET nonexisting
(nil)
redis> SET mykey "Hello"
"OK"
redis> GET mykey
"Hello"
```

### INCR key
Increments the number stored at `key` by one. If the key does not exist, it is set to `0` before performing the operation.
```
redis> SET mykey "10"
"OK"
redis> INCR mykey
(integer) 11
redis> GET mykey
"11"
```

### INCRBY key integer
Increments the number stored at `key` by `increment`. If the key does not exist, it is set to `0` before performing the operation.
```
redis> SET mykey "10"
"OK"
redis> INCRBY mykey 5
(integer) 15
```

### DECR key
Decrements the number stored at `key` by one. If the key does not exist, it is set to `0` before performing the operation.
```
redis> SET mykey "10"
"OK"
redis> DECR mykey
(integer) 9
redis> SET mykey "234293482390480948029348230948"
"OK"
redis> DECR mykey
ERR ERR value is not an integer or out of range
```

### DECRBY key
Decrements the number stored at `key` by `decrement`. If the key does not exist, it is set to `0` before performing the operation.
```
redis> SET mykey "10"
"OK"
redis> DECRBY mykey 3
(integer) 7
```

### APPEND key value
If `key` already exists and is a string, this command appends the `value` at the end of the string. If `key` does not exist it is created and set as an empty string, so APPEND will be similar to SET in this special case.
It returns the length of the string after the append operation.
```
redis> EXISTS mykey
(integer) 0
redis> APPEND mykey "Hello"
(integer) 5
redis> APPEND mykey " World"
(integer) 11
redis> GET mykey
"Hello World"
```

### MSET key value [key value ...]
Sets the given keys to their respective values. MSET replaces existing values with new values, just as regular SET.
```
redis> MSET key1 "Hello" key2 "World"
"OK"
redis> GET key1
"Hello"
redis> GET key2
"World"
```

### MGET key [key ...]
Returns the values of all specified keys. For every key that does not hold a string value or does not exist, the special value `nil` is returned. Because of this, the operation never fails.
```
redis> SET key1 "Hello"
"OK"
redis> SET key2 "World"
"OK"
redis> MGET key1 key2 nonexisting
1) "Hello"
2) "World"
3) (nil)
```

## Authors

-   **Vasco Ramos (nmec 88931)** - [vascoalramos](https://github.com/vascoalramos)
