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

## List
Lists in Redis are ordered collections of Redis strings that allows for duplicates values.

### LPUSH key value [value ...]
Insert all the specified values at the head of the list stored at `key`. If `key` does not exist, it is created as empty list before performing the push operations. When `key` holds a value that is not a list, an error is returned.

It returns the length of the list after the push operations.
```
redis> LPUSH mylist "world"
(integer) 1
redis> LPUSH mylist "hello"
(integer) 2
redis> LRANGE mylist 0 -1
1) "hello"
2) "world"
```

### RPUSH key value [value ...]
Insert all the specified values at the tail of the list stored at `key`. If `key` does not exist, it is created as empty list before performing the push operation. When `key` holds a value that is not a list, an error is returned.

It returns the length of the list after the push operation.
```
redis> RPUSH mylist "hello"
(integer) 1
redis> RPUSH mylist "world"
(integer) 2
redis> LRANGE mylist 0 -1
1) "hello"
2) "world"
```

### LRANGE key start stop
Returns the specified elements of the list stored at `key`. The offsets `start` and `stop` are zero-based indexes, with `0` being the first element of the list (the head of the list), `1` being the next element and so on.

These offsets can also be negative numbers indicating offsets starting at the end of the list. For example, `-1` is the last element of the list, `-2` the penultimate, and so on.
```
redis> RPUSH mylist "one"
(integer) 1
redis> RPUSH mylist "two"
(integer) 2
redis> RPUSH mylist "three"
(integer) 3
redis> LRANGE mylist 0 0
1) "one"
redis> LRANGE mylist -3 2
1) "one"
2) "two"
3) "three"
redis> LRANGE mylist -100 100
1) "one"
2) "two"
3) "three"
redis> LRANGE mylist 5 10
(empty list or set)
```

### LPOP key
Removes and returns the first element of the list stored at `key`

It returns the value of the first element, or `nil` when `key` does not exist.
```
redis> RPUSH mylist "one"
(integer) 1
redis> RPUSH mylist "two"
(integer) 2
redis> RPUSH mylist "three"
(integer) 3
redis> LPOP mylist
"one"
redis> LRANGE mylist 0 -1
1) "two"
2) "three"
```

### RPOP key
Removes and returns the last element of the list stored at `key`.

It returns the value of the last element, or `nil` when `key` does not exist.
```
redis> RPUSH mylist "one"
(integer) 1
redis> RPUSH mylist "two"
(integer) 2
redis> RPUSH mylist "three"
(integer) 3
redis> RPOP mylist
"three"
redis> LRANGE mylist 0 -1
1) "one"
2) "two"
```

### LINDEX key index
Returns the element at index `index` in the list stored at `key`. The index is zero-based, so `0` means the first element, `1` the second element and so on. Negative indices can be used to designate elements starting at the tail of the list. Here, `-1` means the last element, `-2` means the penultimate and so forth.

When the value at `key` is not a list, an error is returned.
```
redis> LPUSH mylist "World"
(integer) 1
redis> LPUSH mylist "Hello"
(integer) 2
redis> LINDEX mylist 0
"Hello"
redis> LINDEX mylist -1
"World"
redis> LINDEX mylist 3
(nil)
```

### LINSERT key BEFORE|AFTER pivot value
Inserts `value` in the list stored at `key` either before or after the reference value `pivot`.

When `key` does not exist, it is considered an empty list and no operation is performed.

An error is returned when `key` exists but does not hold a list value.
```
redis> RPUSH mylist "Hello"
(integer) 1
redis> RPUSH mylist "World"
(integer) 2
redis> LINSERT mylist BEFORE "World" "There"
(integer) 3
redis> LINSERT mylist BEFORE "Nonexistent" "Pivot"
(integer) -1
redis> LRANGE mylist 0 -1
1) "Hello"
2) "There"
3) "World"
```

## Authors

-   **Vasco Ramos (nmec 88931)** - [vascoalramos](https://github.com/vascoalramos)
