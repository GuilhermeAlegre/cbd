# Redis Cheat Sheet


## Table of Contents

 - [Keys](#keys)
	 - [EXISTS key](#exists-key)
	 - [TYPE key](#type-key)
	 - [DEL key](#del-key)
	 - [KEYS pattern](#keys-pattern)
 - [Strings](#strings)
	 - [SET key string optional nx|xx](#set-key-string-optional-nxxx)
	 - [GET key](#get-key)
	 - [INCR key](#incr-key)
	 - [INCRBY key integer](#incrby-key-integer)
	 - [DECR key](#decr-key)
	 - [DECRBY key integer](#decrby-key-integer)
	 - [APPEND key value](#append-key-value)
	 - [MSET key value [key value ...]](#mset-key-value-key-value-...)
	 - [MGET key [key ...]](#mget-key-key-...)
 - [Lists](#lists)
	 - [LPUSH key value [value ...]](#lpush-key-value-value-...)
	 - [RPUSH key value [value ...]](#rpush-key-value-value-...)
	 - [LRANGE key start stop](#lrange-key-start-stop)
	 - [LPOP key](#lpop-key)
	 - [RPOP key](#rpop-key)
	 - [LINDEX key index](#lindex-key-index)
	 - [LINSERT key BEFORE|AFTER pivot value](#linsert-key-beforeafter-pivot-value)
 - [Hash](#hash)
	 - [HSET key field value](#hset-key-field-value)
	 - [HGET key field](#hget-key-field)
	 - [HMSET key field value [field value ...]](#hmset-key-field-value-field-value-...)
	 - [HMGET key field [field ...]](#hmget-key-field-field-...)
	 - [HEXISTS key field](#hexists-key-field)
	 - [HLEN key](#hlen-key)
	 - [HKEYS key](#hkeys-key)
	 - [HVALS key](#hvals-key)
	 - [HDEL key field [field ...]](#hdel-key-field-field-...)
	 - [HINCRBY key field increment](#hincrby-key-field-increment)
 - [Set](#set)
	 - [SADD key member [member ...]](#sadd-key-member-member-...)
	 - [SMEMBERS key](#smembers-key)
	 - [SISMEMBER key member](#sismember-key-member)
	 - [SCARD key](#scard-key)
	 - [SUNION key [key ...]](#sunion-key-key-...)
	 - [SINTER key [key ...]](#sinter-key-key-...)
	 - [ SDIFF key [key ...]](#sdiff-key-key-...)
- [Sorted Set](#sorted-set)
	- [ZADD key [NX|XX] [CH] [INCR] score member [score member ...]](#zadd-key-nxxx-ch-incr-score-member-score-member-...)
	- [ZRANGE key start stop [WITHSCORES]](#zrange-key-start-stop-withscores)
	- [ZREVRANGE key start stop [WITHSCORES]](#zrevrange-key-start-stop-withscores)
	- [ZRANK key member](#zrank-key-member)
	- [ZSCORE key member](#zscore-key-member)
	- [ZREM key member [member ...]](#zrem-key-member-member-...)
	- [ZCARD key](#zcard-key)
	- [ZCOUNT key min max](#zcount-key-min-max)
	- [ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]](#zrangebyscore-key-min-max-withscores-limit-offset-count)
- [Bit array or Bitmap](#bit-array-or-bitmap)
	- [SETBIT key offset value](#setbit-key-offset-value)
	- [GETBIT key offset](#getbit-key-offset)
	- [BITCOUNT key [start end]](#bitcount-key-start-end)
	- [BITPOS key bit [start] [end]](#bitpos-key-bit-start-end)
	- [BITOP operation destkey key [key ...]](#bitop-operation-destkey-key-key-...)
- [HyperLogLogs](#hyperloglogs)
	- [PFADD key element [element ...]](#pfadd-key-element-element-...)
	- [PFCOUNT key [key ...]](#pfcount-key-key-...)
	- [PFMERGE destkey sourcekey [sourcekey ...]](#pfmerge-destkey-sourcekey-sourcekey-...)

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

### KEYS pattern
Returns all keys matching `pattern`.
```
redis> SET testkey "hello"
OK
redis> SET secondkey "hello again"
redis> KEYS *
1) "testkey"
2) "secondkey"
```


## Strings
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

### DECRBY key integer
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


## Lists
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


## Hash

### HSET key field value
Sets `field` in the hash stored at `key` to `value`. If `key` does not exist, a new key holding a hash is created. If `field` already exists in the hash, it is overwritten.

**Return value:**
-   `1` if `field` is a new field in the hash and `value` was set.
-   `0` if `field` already exists in the hash and the value was updated.
```
redis> HSET myhash field1 "Hello"
(integer) 1
redis> HGET myhash field1
"Hello"
```

### HGET key field
Returns the value associated with `field` in the hash stored at `key`.
```
redis> HSET myhash field1 "foo"
(integer) 1
redis> HGET myhash field1
"foo"
redis> HGET myhash field2
(nil)
```

### HMSET key field value [field value ...]
Sets the specified fields to their respective values in the hash stored at `key`. This command overwrites any specified fields already existing in the hash. If `key` does not exist, a new key holding a hash is created.
```
redis> HMSET myhash field1 "Hello" field2 "World"
"OK"
redis> HGET myhash field1
"Hello"
redis> HGET myhash field2
"World"
```

### HMGET key field [field ...]
Returns the values associated with the specified `fields` in the hash stored at `key`.

For every `field` that does not exist in the hash, a `nil` value is returned. Because non-existing keys are treated as empty hashes, running HMGET against a non-existing `key` will return a list of `nil` values.
```
redis> HSET myhash field1 "Hello"
(integer) 1
redis> HSET myhash field2 "World"
(integer) 1
redis> HMGET myhash field1 field2 nofield
1) "Hello"
2) "World"
3) (nil)
```

### HEXISTS key field
Returns if `field` is an existing field in the hash stored at `key`.

**Return value:**
-   `1` if the hash contains `field`.
-   `0` if the hash does not contain `field`, or `key` does not exist.
```
redis> HSET myhash field1 "foo"
(integer) 1
redis> HEXISTS myhash field1
(integer) 1
redis> HEXISTS myhash field2
(integer) 0
```

### HLEN key
Returns the number of fields contained in the hash stored at `key`.
```
redis> HSET myhash field1 "Hello"
(integer) 1
redis> HSET myhash field2 "World"
(integer) 1
redis> HLEN myhash
(integer) 2
```

### HKEYS key
Returns all field names in the hash stored at `key`.
```
redis> HSET myhash field1 "Hello"
(integer) 1
redis> HSET myhash field2 "World"
(integer) 1
redis> HKEYS myhash
1) "field1"
2) "field2"
```

### HVALS key
Returns all values in the hash stored at `key`.
```
redis> HSET myhash field1 "Hello"
(integer) 1
redis> HSET myhash field2 "World"
(integer) 1
redis> HVALS myhash
1) "Hello"
2) "World"
```

### HDEL key field [field ...]
Removes the specified fields from the hash stored at `key`. Specified fields that do not exist within this hash are ignored. If `key` does not exist, it is treated as an empty hash and this command returns `0`.
```
redis> HSET myhash field1 "foo"
(integer) 1
redis> HDEL myhash field1
(integer) 1
redis> HDEL myhash field2
(integer) 0
```

### HINCRBY key field increment
Increments the number stored at `field` in the hash stored at `key` by `increment`. If `key` does not exist, a new key holding a hash is created. If `field` does not exist the value is set to `0` before the operation is performed.
```
redis> HSET myhash field 5
(integer) 1
redis> HINCRBY myhash field 1
(integer) 6
redis> HINCRBY myhash field -1
(integer) 5
redis> HINCRBY myhash field -10
(integer) -5
```


## Set

### SADD key member [member ...]
Add the specified members to the set stored at `key`. Specified members that are already a member of this set are ignored. If `key` does not exist, a new set is created before adding the specified members.

An error is returned when the value stored at `key` is not a set.
```
redis> SADD myset "Hello"
(integer) 1
redis> SADD myset "World"
(integer) 1
redis> SADD myset "World"
(integer) 0
redis> SMEMBERS myset
1) "World"
2) "Hello"
```

### SMEMBERS key
Returns all the members of the set value stored at `key`.

This has the same effect as running SINTER with one argument `key`.
```
redis> SADD myset "Hello"
(integer) 1
redis> SADD myset "World"
(integer) 1
redis> SMEMBERS myset
1) "World"
2) "Hello"
```

### SISMEMBER key member
Returns if `member` is a member of the set stored at `key`.

**Return value:**
-   `1` if the element is a member of the set.
-   `0` if the element is not a member of the set, or if `key` does not exist.
```
redis> SADD myset "one"
(integer) 1
redis> SISMEMBER myset "one"
(integer) 1
redis> SISMEMBER myset "two"
(integer) 0
```

### SCARD key
Returns the set cardinality (number of elements) of the set stored at `key`.
```
redis> SADD myset "Hello"
(integer) 1
redis> SADD myset "World"
(integer) 1
redis> SCARD myset
(integer) 2
```

### SUNION key [key ...]
Returns the members of the set resulting from the union of all the given sets.
```
redis> SADD key1 "a"
(integer) 1
redis> SADD key1 "b"
(integer) 1
redis> SADD key1 "c"
(integer) 1
redis> SADD key2 "c"
(integer) 1
redis> SADD key2 "d"
(integer) 1
redis> SADD key2 "e"
(integer) 1
redis> SUNION key1 key2
1) "b"
2) "c"
3) "d"
4) "a"
5) "e"
```

### SINTER key [key ...]
Returns the members of the set resulting from the intersection of all the given sets.
```
redis> SADD key1 "a"
(integer) 1
redis> SADD key1 "b"
(integer) 1
redis> SADD key1 "c"
(integer) 1
redis> SADD key2 "c"
(integer) 1
redis> SADD key2 "d"
(integer) 1
redis> SADD key2 "e"
(integer) 1
redis> SINTER key1 key2
1) "c"
```

### SDIFF key [key ...]
Returns the members of the set resulting from the difference between the first set and all the successive sets.
```
redis> SADD key1 "a"
(integer) 1
redis> SADD key1 "b"
(integer) 1
redis> SADD key1 "c"
(integer) 1
redis> SADD key2 "c"
(integer) 1
redis> SADD key2 "d"
(integer) 1
redis> SADD key2 "e"
(integer) 1
redis> SDIFF key1 key2
1) "b"
2) "a"
```


## Sorted Set
A sorted set combines characteristics of both Redis lists and sets. Like a Redis list, a sorted set's values are ordered and like a set, each value is assured to be unique. The flexibility of a sorted set allows for multiple types of access patterns depending on the needs of the application.

### ZADD key [NX|XX] [CH] [INCR] score member [score member ...]
Adds all the specified members with the specified scores to the sorted set stored at `key`. It is possible to specify multiple score / member pairs. If a specified member is already a member of the sorted set, the score is updated and the element reinserted at the right position to ensure the correct ordering.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 1 "uno"
(integer) 1
redis> ZADD myzset 2 "two" 3 "three"
(integer) 2
redis> ZRANGE myzset 0 -1 WITHSCORES
1) "one"
2) "1"
3) "uno"
4) "1"
5) "two"
6) "2"
7) "three"
8) "3"
```

### ZRANGE key start stop [WITHSCORES]
Returns the specified range of elements in the sorted set stored at `key`. The elements are considered to be ordered from the lowest to the highest score. Lexicographical order is used for elements with equal score.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 2 "two"
(integer) 1
redis> ZADD myzset 3 "three"
(integer) 1
redis> ZRANGE myzset 0 -1
1) "one"
2) "two"
3) "three"
redis> ZRANGE myzset 2 3
1) "three"
redis> ZRANGE myzset -2 -1
1) "two"
2) "three"
```

### ZREVRANGE key start stop [WITHSCORES]
Returns the specified range of elements in the sorted set stored at `key`. The elements are considered to be ordered from the highest to the lowest score. Descending lexicographical order is used for elements with equal score.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 2 "two"
(integer) 1
redis> ZADD myzset 3 "three"
(integer) 1
redis> ZREVRANGE myzset 0 -1
1) "three"
2) "two"
3) "one"
redis> ZREVRANGE myzset 2 3
1) "one"
redis> ZREVRANGE myzset -2 -1
1) "two"
2) "one"
```

### ZRANK key member
Returns the rank of `member` in the sorted set stored at `key`, with the scores ordered from low to high. The rank (or index) is 0-based, which means that the member with the lowest score has rank `0`.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 2 "two"
(integer) 1
redis> ZADD myzset 3 "three"
(integer) 1
redis> ZRANK myzset "three"
(integer) 2
redis> ZRANK myzset "four"
(nil)
```

### ZSCORE key member
Returns the score of `member` in the sorted set at `key`.

If `member` does not exist in the sorted set, or `key` does not exist, `nil` is returned.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZSCORE myzset "one"
"1"
```

### ZREM key member [member ...]
Removes the specified members from the sorted set stored at `key`. Non existing members are ignored.

An error is returned when `key` exists and does not hold a sorted set.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 2 "two"
(integer) 1
redis> ZADD myzset 3 "three"
(integer) 1
redis> ZREM myzset "two"
(integer) 1
redis> ZRANGE myzset 0 -1 WITHSCORES
1) "one"
2) "1"
3) "three"
4) "3"
```

### ZCARD key
Returns the sorted set cardinality (number of elements) of the sorted set stored at `key`.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 2 "two"
(integer) 1
redis> ZCARD myzset
(integer) 2
```

### ZCOUNT key min max
Returns the number of elements in the sorted set at `key` with a score between `min` and `max`.

```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 2 "two"
(integer) 1
redis> ZADD myzset 3 "three"
(integer) 1
redis> ZCOUNT myzset -inf +inf
(integer) 3
redis> ZCOUNT myzset (1 3
(integer) 2
```

### ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
Returns all the elements in the sorted set at `key` with a score between `min` and `max` (including elements with score equal to `min` or `max`). The elements are considered to be ordered from low to high scores.
```
redis> ZADD myzset 1 "one"
(integer) 1
redis> ZADD myzset 2 "two"
(integer) 1
redis> ZADD myzset 3 "three"
(integer) 1
redis> ZRANGEBYSCORE myzset -inf +inf
1) "one"
2) "two"
3) "three"
redis> ZRANGEBYSCORE myzset 1 2
1) "one"
2) "two"
redis> ZRANGEBYSCORE myzset (1 2
1) "two"
redis> ZRANGEBYSCORE myzset (1 (2
(empty list or set)
```

## Bit array or Bitmap
Redis bitstrings is a very memory efficient data structures in Redis. In a bitstring, 8 bits are stored per byte, with the first bit at position 0 being the significant one that is either set to either 0 or 1. The maximum size for Redis bitstrings is 512 MB.

### SETBIT key offset value
Sets or clears the bit at _offset_ in the string value stored at _key_.
```
redis> SETBIT mykey 7 1
(integer) 0
redis> SETBIT mykey 7 0
(integer) 1
redis> GET mykey
"\u0000"
```

### GETBIT key offset
Returns the bit value at _offset_ in the string value stored at _key_.

When _offset_ is beyond the string length, the string is assumed to be a contiguous space with 0 bits. When _key_ does not exist it is assumed to be an empty string, so _offset_ is always out of range and the value is also assumed to be a contiguous space with 0 bits.
```
redis> SETBIT mykey 7 1
(integer) 0
redis> GETBIT mykey 0
(integer) 0
redis> GETBIT mykey 7
(integer) 1
redis> GETBIT mykey 100
(integer) 0
```

### BITCOUNT key [start end]
Count the number of set bits (population counting) in a string.

By default all the bytes contained in the string are examined. It is possible to specify the counting operation only in an interval passing the additional arguments _start_ and _end_.
```
redis> SET mykey "foobar"
"OK"
redis> BITCOUNT mykey
(integer) 26
redis> BITCOUNT mykey 0 0
(integer) 4
redis> BITCOUNT mykey 1 1
(integer) 6
```

### BITPOS key bit [start] [end]
Return the position of the first bit set to 1 or 0 in a string.

The position is returned, thinking of the string as an array of bits from left to right, where the first byte's most significant bit is at position 0, the second byte's most significant bit is at position 8, and so forth.
```
redis> SET mykey "\xff\xf0\x00"
"OK"
redis> BITPOS mykey 0
(integer) 12
redis> SET mykey "\x00\xff\xf0"
"OK"
redis> BITPOS mykey 1 0
(integer) 8
redis> BITPOS mykey 1 2
(integer) 16
redis> set mykey "\x00\x00\x00"
"OK"
redis> BITPOS mykey 1
(integer) -1
```

### BITOP operation destkey key [key ...]
Perform a bitwise operation between multiple keys (containing string values) and store the result in the destination key.
```
redis> SET key1 "foobar"
"OK"
redis> SET key2 "abcdef"
"OK"
redis> BITOP AND dest key1 key2
(integer) 6
redis> GET dest
"`bc`ab"
```


## HyperLogLogs

### PFADD key element [element ...]
Adds all the element arguments to the HyperLogLog data structure stored at the variable name specified as first argument.
```
redis> PFADD hll a b c d e f g
(integer) 1
redis> PFCOUNT hll
(integer) 7
```

### PFCOUNT key [key ...]
When called with a single key, returns the approximated cardinality computed by the HyperLogLog data structure stored at the specified variable, which is 0 if the variable does not exist.
```
redis> PFADD hll foo bar zap
(integer) 1
redis> PFADD hll zap zap zap
(integer) 0
redis> PFADD hll foo bar
(integer) 0
redis> PFCOUNT hll
(integer) 3
redis> PFADD some-other-hll 1 2 3
(integer) 1
redis> PFCOUNT hll some-other-hll
(integer) 6
```

### PFMERGE destkey sourcekey [sourcekey ...]
Merge multiple HyperLogLog values into an unique value that will approximate the cardinality of the union of the observed Sets of the source HyperLogLog structures.
```
redis> PFADD hll1 foo bar zap a
(integer) 1
redis> PFADD hll2 a b c foo
(integer) 1
redis> PFMERGE hll3 hll1 hll2
"OK"
redis> PFCOUNT hll3
(integer) 6
```

## References and Resources

 - [Introduction to Redis](http://intro2libsys.info/introduction-to-redis/)
 - [Command Reference - Redis](https://redis.io/commands)


## Authors

-   **Vasco Ramos (nmec 88931)** - [vascoalramos](https://github.com/vascoalramos)

