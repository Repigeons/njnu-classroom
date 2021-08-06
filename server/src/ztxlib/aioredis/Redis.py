#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio
import datetime
import time

from aioredis import RedisConnection, RedisError


def list_or_args(keys, args) -> list:
    # returns a single new list combining keys and args
    try:
        iter(keys)
        # a string or bytes instance can be iterated, but indicates
        # keys wasn't passed as a list
        if isinstance(keys, (bytes, str)):
            keys = [keys]
        else:
            keys = list(keys)
    except TypeError:
        keys = [keys]
    if args:
        keys.extend(args)
    return keys


class Redis:
    """
    Implementation of the Redis protocol.

    This abstract class provides a Python interface to all Redis commands
    and an implementation of the Redis protocol.

    Connection and Pipeline derive from this, implementing how
    the commands are sent and received to the Redis server
    """

    def __init__(self, connection: RedisConnection):
        self.connection = connection

    def __repr__(self):
        return "<%s%s>" % (type(self).__name__, repr(self.connection))

    def __setitem__(self, name, value):
        asyncio.run(self.set(name, value))

    def __delitem__(self, name):
        asyncio.run(self.delete(name))

    def __getitem__(self, name):
        """
        Return the value at key ``name``, raises a KeyError if the key
        doesn't exist.
        """
        loop = asyncio.get_event_loop()
        value = loop.run_until_complete(self.get(name))
        if value is not None:
            return value
        raise KeyError(name)

    def close(self):
        self.connection = None

    # ACL methods
    async def acl_cat(self, category=None):
        """
        Returns a list of categories or commands within a category.

        If ``category`` is not supplied, returns a list of all categories.
        If ``category`` is supplied, returns a list of all commands within
        that category.
        """
        pieces = [category] if category else []
        return await self.connection.execute('ACL CAT', *pieces)

    async def acl_deluser(self, username):
        """
        Delete the ACL for the specified ``username``
        """
        return await self.connection.execute('ACL DELUSER', username)

    async def acl_genpass(self):
        """
        Generate a random password value
        """
        return await self.connection.execute('ACL GENPASS')

    async def acl_getuser(self, username):
        """
        Get the ACL details for the specified ``username``.

        If ``username`` does not exist, return None
        """
        return await self.connection.execute('ACL GETUSER', username)

    async def acl_list(self):
        """
        Return a list of all ACLs on the server
        """
        return await self.connection.execute('ACL LIST')

    async def acl_load(self):
        """
        Load ACL rules from the configured ``aclfile``.

        Note that the server must be configured with the ``aclfile``
        directive to be able to load ACL rules from an aclfile.
        """
        return await self.connection.execute('ACL LOAD')

    async def acl_save(self):
        """
        Save ACL rules to the configured ``aclfile``.

        Note that the server must be configured with the ``aclfile``
        directive to be able to save ACL rules to an aclfile.
        """
        return await self.connection.execute('ACL SAVE')

    async def acl_users(self):
        """
        Returns a list of all registered users on the server.
        """
        return await self.connection.execute('ACL USERS')

    async def acl_whoami(self):
        """
        Get the username for the current connection
        """
        return await self.connection.execute('ACL WHOAMI')

    async def bgrewriteaof(self):
        """
        Tell the Redis server to rewrite the AOF file from data in memory.
        """
        return await self.connection.execute('BGREWRITEAOF')

    async def bgsave(self):
        """
        Tell the Redis server to save its data to disk.  Unlike save(),
        this method is asynchronous and returns immediately.
        """
        return await self.connection.execute('BGSAVE')

    async def client_kill(self, address):
        """
        Disconnects the client at ``address`` (ip:port)
        """
        return await self.connection.execute('CLIENT KILL', address)

    async def client_kill_filter(self, _id=None, _type=None, addr=None, skipme=None):
        """
        Disconnects client(s) using a variety of filter options
        :param _id: Kills a client by its unique ID field
        :param _type: Kills a client by type where type is one of 'normal',
        'master', 'slave' or 'pubsub'
        :param addr: Kills a client by its 'address:port'
        :param skipme: If True, then the client calling the command
        will not get killed even if it is identified by one of the filter
        options. If skipme is not provided, the server defaults to skipme=True
        """
        args = []
        if _type is not None:
            client_types = ('normal', 'master', 'slave', 'pubsub')
            if str(_type).lower() not in client_types:
                raise RedisError("CLIENT KILL type must be one of %r" % (
                    client_types,))
            args.extend((b'TYPE', _type))
        if skipme is not None:
            if not isinstance(skipme, bool):
                raise RedisError("CLIENT KILL skipme must be a bool")
            if skipme:
                args.extend((b'SKIPME', b'YES'))
            else:
                args.extend((b'SKIPME', b'NO'))
        if _id is not None:
            args.extend((b'ID', _id))
        if addr is not None:
            args.extend((b'ADDR', addr))
        if not args:
            raise RedisError("CLIENT KILL <filter> <value> ... ... <filter> "
                             "<value> must specify at least one filter")
        return await self.connection.execute('CLIENT KILL', *args)

    async def client_list(self, _type=None):
        """
        Returns a list of currently connected clients.
        If type of client specified, only that type will be returned.
        :param _type: optional. one of the client types (normal, master,
         replica, pubsub)
        """
        "Returns a list of currently connected clients"
        if _type is not None:
            client_types = ('normal', 'master', 'replica', 'pubsub')
            if str(_type).lower() not in client_types:
                raise RedisError("CLIENT LIST _type must be one of %r" % (
                    client_types,))
            return await self.connection.execute('CLIENT LIST', b'TYPE', _type)
        return await self.connection.execute('CLIENT LIST')

    async def client_getname(self):
        """
        Returns the current connection name
        """
        return await self.connection.execute('CLIENT GETNAME')

    async def client_id(self):
        """
        Returns the current connection id
        """
        return await self.connection.execute('CLIENT ID')

    async def client_setname(self, name):
        """
        Sets the current connection name
        """
        return await self.connection.execute('CLIENT SETNAME', name)

    async def client_unblock(self, client_id, error=False):
        """
        Unblocks a connection by its client id.
        If ``error`` is True, unblocks the client with a special error message.
        If ``error`` is False (default), the client is unblocked using the
        regular timeout mechanism.
        """
        args = ['CLIENT UNBLOCK', int(client_id)]
        if error:
            args.append(b'ERROR')
        return await self.connection.execute(*args)

    async def client_pause(self, timeout):
        """
        Suspend all the Redis clients for the specified amount of time
        :param timeout: milliseconds to pause clients
        """
        if not isinstance(timeout, int):
            raise RedisError("CLIENT PAUSE timeout must be an integer")
        return await self.connection.execute('CLIENT PAUSE', str(timeout))

    async def readwrite(self):
        """
        Disables read queries for a connection to a Redis Cluster slave node
        """
        return await self.connection.execute('READWRITE')

    async def readonly(self):
        """
        Enables read queries for a connection to a Redis Cluster replica node
        """
        return await self.connection.execute('READONLY')

    async def config_get(self, pattern="*"):
        """
        Return a dictionary of configuration based on the ``pattern``
        """
        return await self.connection.execute('CONFIG GET', pattern)

    async def config_set(self, name, value):
        """
        Set config item ``name`` with ``value``
        """
        return await self.connection.execute('CONFIG SET', name, value)

    async def config_resetstat(self):
        """
        Reset runtime statistics
        """
        return await self.connection.execute('CONFIG RESETSTAT')

    async def config_rewrite(self):
        """
        Rewrite config file with the minimal change to reflect running config
        """
        return await self.connection.execute('CONFIG REWRITE')

    async def dbsize(self):
        """
        Returns the number of keys in the current database
        """
        return await self.connection.execute('DBSIZE')

    async def debug_object(self, key):
        """
        Returns version specific meta information about a given key
        """
        return await self.connection.execute('DEBUG OBJECT', key)

    async def echo(self, value):
        """
        Echo the string back from the server
        """
        return await self.connection.execute('ECHO', value)

    async def flushall(self, asynchronous=False):
        """
        Delete all keys in all databases on the current host.

        ``asynchronous`` indicates whether the operation is
        executed asynchronously by the server.
        """
        args = []
        if asynchronous:
            args.append(b'ASYNC')
        return await self.connection.execute('FLUSHALL', *args)

    async def flushdb(self, asynchronous=False):
        """
        Delete all keys in the current database.

        ``asynchronous`` indicates whether the operation is
        executed asynchronously by the server.
        """
        args = []
        if asynchronous:
            args.append(b'ASYNC')
        return await self.connection.execute('FLUSHDB', *args)

    async def swapdb(self, first, second):
        """
        Swap two databases
        """
        return await self.connection.execute('SWAPDB', first, second)

    async def info(self, section=None):
        """
        Returns a dictionary containing information about the Redis server

        The ``section`` option can be used to select a specific section
        of information

        The section option is not supported by older versions of Redis Server,
        and will generate ResponseError
        """
        if section is None:
            return await self.connection.execute('INFO')
        else:
            return await self.connection.execute('INFO', section)

    async def lastsave(self):
        """
        Return a Python datetime object representing the last time the
        Redis database was saved to disk
        """
        return await self.connection.execute('LASTSAVE')

    async def migrate(self, host, port, keys, destination_db, timeout,
                      copy=False, replace=False, auth=None):
        """
        Migrate 1 or more keys from the current Redis server to a different
        server specified by the ``host``, ``port`` and ``destination_db``.

        The ``timeout``, specified in milliseconds, indicates the maximum
        time the connection between the two servers can be idle before the
        command is interrupted.

        If ``copy`` is True, the specified ``keys`` are NOT deleted from
        the source server.

        If ``replace`` is True, this operation will overwrite the keys
        on the destination server if they exist.

        If ``auth`` is specified, authenticate to the destination server with
        the password provided.
        """
        keys = list_or_args(keys, [])
        if not keys:
            raise RedisError('MIGRATE requires at least one key')
        pieces = []
        if copy:
            pieces.append(b'COPY')
        if replace:
            pieces.append(b'REPLACE')
        if auth:
            pieces.append(b'AUTH')
            pieces.append(auth)
        pieces.append(b'KEYS')
        pieces.extend(keys)
        return await self.connection.execute('MIGRATE', host, port, '', destination_db,
                                             timeout, *pieces)

    async def memory_stats(self):
        """
        Return a dictionary of memory stats
        """
        return await self.connection.execute('MEMORY STATS')

    async def memory_usage(self, key, samples=None):
        """
        Return the total memory usage for key, its value and associated
        administrative overheads.

        For nested data structures, ``samples`` is the number of elements to
        sample. If left unspecified, the server's default is 5. Use 0 to sample
        all elements.
        """
        args = []
        if isinstance(samples, int):
            args.extend([b'SAMPLES', samples])
        return await self.connection.execute('MEMORY USAGE', key, *args)

    async def memory_purge(self):
        """
        Attempts to purge dirty pages for reclamation by allocator
        """
        return await self.connection.execute('MEMORY PURGE')

    async def ping(self):
        """
        Ping the Redis server
        """
        return await self.connection.execute('PING')

    async def save(self):
        """
        Tell the Redis server to save its data to disk,
        blocking until the save is complete
        """
        return await self.connection.execute('SAVE')

    async def sentinel_get_master_addr_by_name(self, service_name):
        """
        Returns a (host, port) pair for the given ``service_name``
        """
        return await self.connection.execute('SENTINEL GET-MASTER-ADDR-BY-NAME',
                                             service_name)

    async def sentinel_master(self, service_name):
        """
        Returns a dictionary containing the specified masters state.
        """
        return await self.connection.execute('SENTINEL MASTER', service_name)

    async def sentinel_masters(self):
        """
        Returns a list of dictionaries containing each master's state.
        """
        return await self.connection.execute('SENTINEL MASTERS')

    async def sentinel_monitor(self, name, ip, port, quorum):
        """
        Add a new master to Sentinel to be monitored
        """
        return await self.connection.execute('SENTINEL MONITOR', name, ip, port, quorum)

    async def sentinel_remove(self, name):
        """
        Remove a master from Sentinel's monitoring
        """
        return await self.connection.execute('SENTINEL REMOVE', name)

    async def sentinel_sentinels(self, service_name):
        """
        Returns a list of sentinels for ``service_name``
        """
        return await self.connection.execute('SENTINEL SENTINELS', service_name)

    async def sentinel_set(self, name, option, value):
        """
        Set Sentinel monitoring parameters for a given master
        """
        return await self.connection.execute('SENTINEL SET', name, option, value)

    async def sentinel_slaves(self, service_name):
        """
        Returns a list of slaves for ``service_name``
        """
        return await self.connection.execute('SENTINEL SLAVES', service_name)

    async def shutdown(self, save=False, nosave=False):
        """Shutdown the Redis server.  If Redis has persistence configured,
        data will be flushed before shutdown.  If the "save" option is set,
        a data flush will be attempted even if there is no persistence
        configured.  If the "nosave" option is set, no data flush will be
        attempted.  The "save" and "nosave" options cannot both be set.
        """
        if save and nosave:
            raise RedisError('SHUTDOWN save and nosave cannot both be set')
        args = ['SHUTDOWN']
        if save:
            args.append('SAVE')
        if nosave:
            args.append('NOSAVE')
        try:
            await self.connection.execute(*args)
        except ConnectionError:
            # a ConnectionError here is expected
            return
        raise RedisError("SHUTDOWN seems to have failed.")

    async def slaveof(self, host=None, port=None):
        """
        Set the server to be a replicated slave of the instance identified
        by the ``host`` and ``port``. If called without arguments, the
        instance is promoted to a master instead.
        """
        if host is None and port is None:
            return await self.connection.execute('SLAVEOF', b'NO', b'ONE')
        return await self.connection.execute('SLAVEOF', host, port)

    async def slowlog_len(self):
        """
        Get the number of items in the slowlog
        """
        return await self.connection.execute('SLOWLOG LEN')

    async def slowlog_reset(self):
        """
        Remove all items in the slowlog
        """
        return await self.connection.execute('SLOWLOG RESET')

    async def time(self):
        """
        Returns the server time as a 2-item tuple of ints:
        (seconds since epoch, microseconds into this second).
        """
        return await self.connection.execute('TIME')

    async def wait(self, num_replicas, timeout):
        """
        Redis synchronous replication
        That returns the number of replicas that processed the query when
        we finally have at least ``num_replicas``, or when the ``timeout`` was
        reached.
        """
        return await self.connection.execute('WAIT', num_replicas, timeout)

    # BASIC KEY COMMANDS
    async def append(self, key, value):
        """
        Appends the string ``value`` to the value at ``key``. If ``key``
        doesn't already exist, create it with a value of ``value``.
        Returns the new length of the value at ``key``.
        """
        return await self.connection.execute('APPEND', key, value)

    async def bitcount(self, key, start=None, end=None):
        """
        Returns the count of set bits in the value of ``key``.  Optional
        ``start`` and ``end`` paramaters indicate which bytes to consider
        """
        params = [key]
        if start is not None and end is not None:
            params.append(start)
            params.append(end)
        elif (start is not None and end is None) or \
                (end is not None and start is None):
            raise RedisError("Both start and end must be specified")
        return await self.connection.execute('BITCOUNT', *params)

    async def bitop(self, operation, dest, *keys):
        """
        Perform a bitwise operation using ``operation`` between ``keys`` and
        store the result in ``dest``.
        """
        return await self.connection.execute('BITOP', operation, dest, *keys)

    async def bitpos(self, key, bit, start=None, end=None):
        """
        Return the position of the first bit set to 1 or 0 in a string.
        ``start`` and ``end`` difines search range. The range is interpreted
        as a range of bytes and not a range of bits, so start=0 and end=2
        means to look at the first three bytes.
        """
        if bit not in (0, 1):
            raise RedisError('bit must be 0 or 1')
        params = [key, bit]

        start is not None and params.append(start)

        if start is not None and end is not None:
            params.append(end)
        elif start is None and end is not None:
            raise RedisError("start argument is not set, "
                             "when end is specified")
        return await self.connection.execute('BITPOS', *params)

    async def decr(self, name, amount=1):
        """
        Decrements the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as 0 - ``amount``
        """
        # An alias for ``decr()``, because it is already implemented
        # as DECRBY redis command.
        return self.decrby(name, amount)

    async def decrby(self, name, amount=1):
        """
        Decrements the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as 0 - ``amount``
        """
        return await self.connection.execute('DECRBY', name, amount)

    async def delete(self, *names):
        """
        Delete one or more keys specified by ``names``
        """
        return await self.connection.execute('DEL', *names)

    async def dump(self, name):
        """
        Return a serialized version of the value stored at the specified key.
        If key does not exist a nil bulk reply is returned.
        """
        return await self.connection.execute('DUMP', name)

    async def exists(self, *names):
        """
        Returns the number of ``names`` that exist
        """
        return await self.connection.execute('EXISTS', *names)

    __contains__ = exists

    async def expire(self, name, expire):
        """
        Set an expire flag on key ``name`` for ``time`` seconds. ``time``
        can be represented by an integer or a Python timedelta object.
        """
        if isinstance(expire, datetime.timedelta):
            expire = int(expire.total_seconds())
        return await self.connection.execute('EXPIRE', name, expire)

    async def expireat(self, name, when):
        """
        Set an expire flag on key ``name``. ``when`` can be represented
        as an integer indicating unix time or a Python datetime object.
        """
        if isinstance(when, datetime.datetime):
            when = int(time.mktime(when.timetuple()))
        return await self.connection.execute('EXPIREAT', name, when)

    async def get(self, name):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        return await self.connection.execute('GET', name)

    async def getbit(self, name, offset):
        """
        Returns a boolean indicating the value of ``offset`` in ``name``
        """
        return await self.connection.execute('GETBIT', name, offset)

    async def getrange(self, key, start, end):
        """
        Returns the substring of the string value stored at ``key``,
        determined by the offsets ``start`` and ``end`` (both are inclusive)
        """
        return await self.connection.execute('GETRANGE', key, start, end)

    async def getset(self, name, value):
        """
        Sets the value at key ``name`` to ``value``
        and returns the old value at key ``name`` atomically.
        """
        return await self.connection.execute('GETSET', name, value)

    async def incr(self, name, amount=1):
        """
        Increments the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as ``amount``
        """
        return self.incrby(name, amount)

    async def incrby(self, name, amount=1):
        """
        Increments the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as ``amount``
        """
        # An alias for ``incr()``, because it is already implemented
        # as INCRBY redis command.
        return await self.connection.execute('INCRBY', name, amount)

    async def incrbyfloat(self, name, amount=1.0):
        """
        Increments the value at key ``name`` by floating ``amount``.
        If no key exists, the value will be initialized as ``amount``
        """
        return await self.connection.execute('INCRBYFLOAT', name, amount)

    async def keys(self, pattern='*'):
        """
        Returns a list of keys matching ``pattern``
        """
        return await self.connection.execute('KEYS', pattern)

    async def mget(self, keys, *args):
        """
        Returns a list of values ordered identically to ``keys``
        """
        args = list_or_args(keys, args)
        options = {}
        if not args:
            options['EMPTY_RESPONSE'] = []
        return await self.connection.execute('MGET', *args, **options)

    async def mset(self, mapping):
        """
        Sets key/values based on a mapping. Mapping is a dictionary of
        key/value pairs. Both keys and values should be strings or types that
        can be cast to a string via str().
        """
        items = []
        for pair in iter(mapping.items()):
            items.extend(pair)
        return await self.connection.execute('MSET', *items)

    async def msetnx(self, mapping):
        """
        Sets key/values based on a mapping if none of the keys are already set.
        Mapping is a dictionary of key/value pairs. Both keys and values
        should be strings or types that can be cast to a string via str().
        Returns a boolean indicating if the operation was successful.
        """
        items = []
        for pair in iter(mapping.items()):
            items.extend(pair)
        return await self.connection.execute('MSETNX', *items)

    async def move(self, name, db):
        """
        Moves the key ``name`` to a different Redis database ``db``
        """
        return await self.connection.execute('MOVE', name, db)

    async def persist(self, name):
        """
        Removes an expiration on ``name``
        """
        return await self.connection.execute('PERSIST', name)

    async def pexpire(self, name, expire):
        """
        Set an expire flag on key ``name`` for ``time`` milliseconds.
        ``time`` can be represented by an integer or a Python timedelta
        object.
        """
        if isinstance(expire, datetime.timedelta):
            expire = int(expire.total_seconds() * 1000)
        return await self.connection.execute('PEXPIRE', name, expire)

    async def pexpireat(self, name, when):
        """
        Set an expire flag on key ``name``. ``when`` can be represented
        as an integer representing unix time in milliseconds (unix time * 1000)
        or a Python datetime object.
        """
        if isinstance(when, datetime.datetime):
            ms = int(when.microsecond / 1000)
            when = int(time.mktime(when.timetuple())) * 1000 + ms
        return await self.connection.execute('PEXPIREAT', name, when)

    async def psetex(self, name, time_ms, value):
        """
        Set the value of key ``name`` to ``value`` that expires in ``time_ms``
        milliseconds. ``time_ms`` can be represented by an integer or a Python
        timedelta object
        """
        if isinstance(time_ms, datetime.timedelta):
            time_ms = int(time_ms.total_seconds() * 1000)
        return await self.connection.execute('PSETEX', name, time_ms, value)

    async def pttl(self, name):
        """
        Returns the number of milliseconds until the key ``name`` will expire
        """
        return await self.connection.execute('PTTL', name)

    async def randomkey(self):
        """
        Returns the name of a random key
        """
        return await self.connection.execute('RANDOMKEY')

    async def rename(self, src, dst):
        """
        Rename key ``src`` to ``dst``
        """
        return await self.connection.execute('RENAME', src, dst)

    async def renamenx(self, src, dst):
        """
        Rename key ``src`` to ``dst`` if ``dst`` doesn't already exist
        """
        return await self.connection.execute('RENAMENX', src, dst)

    async def restore(self, name, ttl, value, replace=False):
        """
        Create a key using the provided serialized value, previously obtained
        using DUMP.
        """
        params = [name, ttl, value]
        if replace:
            params.append('REPLACE')
        return await self.connection.execute('RESTORE', *params)

    async def set(self, name, value,
                  ex=None, px=None, nx=False, xx=False, keepttl=False):
        """
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.

        ``keepttl`` if True, retain the time to live associated with the key.
            (Available since Redis 6.0)
        """
        pieces = [name, value]
        if ex is not None:
            pieces.append('EX')
            if isinstance(ex, datetime.timedelta):
                ex = int(ex.total_seconds())
            pieces.append(ex)
        if px is not None:
            pieces.append('PX')
            if isinstance(px, datetime.timedelta):
                px = int(px.total_seconds() * 1000)
            pieces.append(px)

        if nx:
            pieces.append('NX')
        if xx:
            pieces.append('XX')

        if keepttl:
            pieces.append('KEEPTTL')

        return await self.connection.execute('SET', *pieces)

    async def setbit(self, name, offset, value):
        """
        Flag the ``offset`` in ``name`` as ``value``. Returns a boolean
        indicating the previous value of ``offset``.
        """
        value = value and 1 or 0
        return await self.connection.execute('SETBIT', name, offset, value)

    async def setex(self, name, expire, value):
        """
        Set the value of key ``name`` to ``value`` that expires in ``time``
        seconds. ``time`` can be represented by an integer or a Python
        timedelta object.
        """
        if isinstance(expire, datetime.timedelta):
            expire = int(expire.total_seconds())
        return await self.connection.execute('SETEX', name, expire, value)

    async def setnx(self, name, value):
        """
        Set the value of key ``name`` to ``value`` if key doesn't exist
        """
        return await self.connection.execute('SETNX', name, value)

    async def setrange(self, name, offset, value):
        """
        Overwrite bytes in the value of ``name`` starting at ``offset`` with
        ``value``. If ``offset`` plus the length of ``value`` exceeds the
        length of the original value, the new value will be larger than before.
        If ``offset`` exceeds the length of the original value, null bytes
        will be used to pad between the end of the previous value and the start
        of what's being injected.

        Returns the length of the new string.
        """
        return await self.connection.execute('SETRANGE', name, offset, value)

    async def strlen(self, name):
        """
        Return the number of bytes stored in the value of ``name``
        """
        return await self.connection.execute('STRLEN', name)

    async def substr(self, name, start, end=-1):
        """
        Return a substring of the string at key ``name``. ``start`` and ``end``
        are 0-based integers specifying the portion of the string to return.
        """
        return await self.connection.execute('SUBSTR', name, start, end)

    async def touch(self, *args):
        """
        Alters the last access time of a key(s) ``*args``. A key is ignored
        if it does not exist.
        """
        return await self.connection.execute('TOUCH', *args)

    async def ttl(self, name):
        """
        Returns the number of seconds until the key ``name`` will expire
        """
        return await self.connection.execute('TTL', name)

    async def type(self, name):
        """
        Returns the type of key ``name``
        """
        return await self.connection.execute('TYPE', name)

    async def unlink(self, *names):
        """
        Unlink one or more keys specified by ``names``
        """
        return await self.connection.execute('UNLINK', *names)

    # LIST COMMANDS
    async def blpop(self, keys, timeout=0):
        """
        LPOP a value off of the first non-empty list
        named in the ``keys`` list.

        If none of the lists in ``keys`` has a value to LPOP, then block
        for ``timeout`` seconds, or until a value gets pushed on to one
        of the lists.

        If timeout is 0, then block indefinitely.
        """
        if timeout is None:
            timeout = 0
        keys = list_or_args(keys, None)
        keys.append(timeout)
        return await self.connection.execute('BLPOP', *keys)

    async def brpop(self, keys, timeout=0):
        """
        RPOP a value off of the first non-empty list
        named in the ``keys`` list.

        If none of the lists in ``keys`` has a value to RPOP, then block
        for ``timeout`` seconds, or until a value gets pushed on to one
        of the lists.

        If timeout is 0, then block indefinitely.
        """
        if timeout is None:
            timeout = 0
        keys = list_or_args(keys, None)
        keys.append(timeout)
        return await self.connection.execute('BRPOP', *keys)

    async def brpoplpush(self, src, dst, timeout=0):
        """
        Pop a value off the tail of ``src``, push it on the head of ``dst``
        and then return it.

        This command blocks until a value is in ``src`` or until ``timeout``
        seconds elapse, whichever is first. A ``timeout`` value of 0 blocks
        forever.
        """
        if timeout is None:
            timeout = 0
        return await self.connection.execute('BRPOPLPUSH', src, dst, timeout)

    async def lindex(self, name, index):
        """
        Return the item from list ``name`` at position ``index``

        Negative indexes are supported and will return an item at the
        end of the list
        """
        return await self.connection.execute('LINDEX', name, index)

    async def linsert(self, name, where, refvalue, value):
        """
        Insert ``value`` in list ``name`` either immediately before or after
        [``where``] ``refvalue``

        Returns the new length of the list on success or -1 if ``refvalue``
        is not in the list.
        """
        return await self.connection.execute('LINSERT', name, where, refvalue, value)

    async def llen(self, name):
        """
        Return the length of the list ``name``
        """
        return await self.connection.execute('LLEN', name)

    async def lpop(self, name):
        """
        Remove and return the first item of the list ``name``
        """
        return await self.connection.execute('LPOP', name)

    async def lpush(self, name, *values):
        """
        Push ``values`` onto the head of the list ``name``
        """
        return await self.connection.execute('LPUSH', name, *values)

    async def lpushx(self, name, value):
        """
        Push ``value`` onto the head of the list ``name`` if ``name`` exists
        """
        return await self.connection.execute('LPUSHX', name, value)

    async def lrange(self, name, start, end):
        """
        Return a slice of the list ``name`` between
        position ``start`` and ``end``

        ``start`` and ``end`` can be negative numbers just like
        Python slicing notation
        """
        return await self.connection.execute('LRANGE', name, start, end)

    async def lrem(self, name, count, value):
        """
        Remove the first ``count`` occurrences of elements equal to ``value``
        from the list stored at ``name``.

        The count argument influences the operation in the following ways:
            count > 0: Remove elements equal to value moving from head to tail.
            count < 0: Remove elements equal to value moving from tail to head.
            count = 0: Remove all elements equal to value.
        """
        return await self.connection.execute('LREM', name, count, value)

    async def lset(self, name, index, value):
        """
        Set ``position`` of list ``name`` to ``value``
        """
        return await self.connection.execute('LSET', name, index, value)

    async def ltrim(self, name, start, end):
        """
        Trim the list ``name``, removing all values not within the slice
        between ``start`` and ``end``

        ``start`` and ``end`` can be negative numbers just like
        Python slicing notation
        """
        return await self.connection.execute('LTRIM', name, start, end)

    async def rpop(self, name):
        """
        Remove and return the last item of the list ``name``
        """
        return await self.connection.execute('RPOP', name)

    async def rpoplpush(self, src, dst):
        """
        RPOP a value off of the ``src`` list and atomically LPUSH it
        on to the ``dst`` list.  Returns the value.
        """
        return await self.connection.execute('RPOPLPUSH', src, dst)

    async def rpush(self, name, *values):
        """
        Push ``values`` onto the tail of the list ``name``
        """
        return await self.connection.execute('RPUSH', name, *values)

    async def rpushx(self, name, value):
        """
        Push ``value`` onto the tail of the list ``name`` if ``name`` exists
        """
        return await self.connection.execute('RPUSHX', name, value)

    async def sort(self, name, start=None, num=None, by=None, get=None,
                   desc=False, alpha=False, store=None, groups=False):
        """
        Sort and return the list, set or sorted set at ``name``.

        ``start`` and ``num`` allow for paging through the sorted data

        ``by`` allows using an external key to weight and sort the items.
            Use an "*" to indicate where in the key the item value is located

        ``get`` allows for returning items from external keys rather than the
            sorted data itself.  Use an "*" to indicate where in the key
            the item value is located

        ``desc`` allows for reversing the sort

        ``alpha`` allows for sorting lexicographically rather than numerically

        ``store`` allows for storing the result of the sort into
            the key ``store``

        ``groups`` if set to True and if ``get`` contains at least two
            elements, sort will return a list of tuples, each containing the
            values fetched from the arguments to ``get``.

        """
        if (start is not None and num is None) or \
                (num is not None and start is None):
            raise RedisError("``start`` and ``num`` must both be specified")

        pieces = [name]
        if by is not None:
            pieces.append(b'BY')
            pieces.append(by)
        if start is not None and num is not None:
            pieces.append(b'LIMIT')
            pieces.append(start)
            pieces.append(num)

        # If get is a string assume we want to get a single value.
        # Otherwise assume it's an interable and we want to get multiple
        # values. We can't just iterate blindly because strings are
        # iterable.
        if isinstance(get, (bytes, str)):
            pieces.append(b'GET')
            pieces.append(get)
        elif get is not None:
            for g in get:
                pieces.append(b'GET')
                pieces.append(g)
        if desc:
            pieces.append(b'DESC')
        if alpha:
            pieces.append(b'ALPHA')
        if store is not None:
            pieces.append(b'STORE')
            pieces.append(store)

        if groups:
            if not get or isinstance(get, (bytes, str)) or len(get) < 2:
                raise RedisError('when using "groups" the "get" argument '
                                 'must be specified and contain at least '
                                 'two keys')

        options = {'groups': len(get) if groups else None}
        return await self.connection.execute('SORT', *pieces, **options)

    # SCAN COMMANDS
    async def scan(self, cursor=0, match=None, count=None, _type=None):
        """
        Incrementally return lists of key names. Also return a cursor
        indicating the scan position.

        ``match`` allows for filtering the keys by pattern

        ``count`` provides a hint to Redis about the number of keys to
            return per batch.

        ``_type`` filters the returned values by a particular Redis type.
            Stock Redis instances allow for the following types:
            HASH, LIST, SET, STREAM, STRING, ZSET
            Additionally, Redis modules can expose other types as well.
        """
        pieces = [cursor]
        if match is not None:
            pieces.extend([b'MATCH', match])
        if count is not None:
            pieces.extend([b'COUNT', count])
        if _type is not None:
            pieces.extend([b'TYPE', _type])
        return await self.connection.execute('SCAN', *pieces)

    async def scan_iter(self, match=None, count=None, _type=None):
        """
        Make an iterator using the SCAN command so that the client doesn't
        need to remember the cursor position.

        ``match`` allows for filtering the keys by pattern

        ``count`` provides a hint to Redis about the number of keys to
            return per batch.

        ``_type`` filters the returned values by a particular Redis type.
            Stock Redis instances allow for the following types:
            HASH, LIST, SET, STREAM, STRING, ZSET
            Additionally, Redis modules can expose other types as well.
        """
        cursor = '0'
        while cursor != 0:
            cursor, data = self.scan(cursor=cursor, match=match,
                                     count=count, _type=_type)
            for item in data:
                yield item

    async def sscan(self, name, cursor=0, match=None, count=None):
        """
        Incrementally return lists of elements in a set. Also return a cursor
        indicating the scan position.

        ``match`` allows for filtering the keys by pattern

        ``count`` allows for hint the minimum number of returns
        """
        pieces = [name, cursor]
        if match is not None:
            pieces.extend([b'MATCH', match])
        if count is not None:
            pieces.extend([b'COUNT', count])
        return await self.connection.execute('SSCAN', *pieces)

    async def sscan_iter(self, name, match=None, count=None):
        """
        Make an iterator using the SSCAN command so that the client doesn't
        need to remember the cursor position.

        ``match`` allows for filtering the keys by pattern

        ``count`` allows for hint the minimum number of returns
        """
        cursor = '0'
        while cursor != 0:
            cursor, data = self.sscan(name, cursor=cursor,
                                      match=match, count=count)
            for item in data:
                yield item

    async def hscan(self, name, cursor=0, match=None, count=None):
        """
        Incrementally return key/value slices in a hash. Also return a cursor
        indicating the scan position.

        ``match`` allows for filtering the keys by pattern

        ``count`` allows for hint the minimum number of returns
        """
        pieces = [name, cursor]
        if match is not None:
            pieces.extend([b'MATCH', match])
        if count is not None:
            pieces.extend([b'COUNT', count])
        return await self.connection.execute('HSCAN', *pieces)

    async def hscan_iter(self, name, match=None, count=None):
        """
        Make an iterator using the HSCAN command so that the client doesn't
        need to remember the cursor position.

        ``match`` allows for filtering the keys by pattern

        ``count`` allows for hint the minimum number of returns
        """
        cursor = '0'
        while cursor != 0:
            cursor, data = self.hscan(name, cursor=cursor,
                                      match=match, count=count)
            for item in data.items():
                yield item

    async def zscan(self, name, cursor=0, match=None, count=None,
                    score_cast_func=float):
        """
        Incrementally return lists of elements in a sorted set. Also return a
        cursor indicating the scan position.

        ``match`` allows for filtering the keys by pattern

        ``count`` allows for hint the minimum number of returns

        ``score_cast_func`` a callable used to cast the score return value
        """
        pieces = [name, cursor]
        if match is not None:
            pieces.extend([b'MATCH', match])
        if count is not None:
            pieces.extend([b'COUNT', count])
        options = {'score_cast_func': score_cast_func}
        return await self.connection.execute('ZSCAN', *pieces, **options)

    async def zscan_iter(self, name, match=None, count=None,
                         score_cast_func=float):
        """
        Make an iterator using the ZSCAN command so that the client doesn't
        need to remember the cursor position.

        ``match`` allows for filtering the keys by pattern

        ``count`` allows for hint the minimum number of returns

        ``score_cast_func`` a callable used to cast the score return value
        """
        cursor = '0'
        while cursor != 0:
            cursor, data = self.zscan(name, cursor=cursor, match=match,
                                      count=count,
                                      score_cast_func=score_cast_func)
            for item in data:
                yield item

    # SET COMMANDS
    async def sadd(self, name, *values):
        """
        Add ``value(s)`` to set ``name``
        """
        return await self.connection.execute('SADD', name, *values)

    async def scard(self, name):
        """
        Return the number of elements in set ``name``
        """
        return await self.connection.execute('SCARD', name)

    async def sdiff(self, keys, *args):
        """
        Return the difference of sets specified by ``keys``
        """
        args = list_or_args(keys, args)
        return await self.connection.execute('SDIFF', *args)

    async def sdiffstore(self, dest, keys, *args):
        """
        Store the difference of sets specified by ``keys`` into a new
        set named ``dest``.  Returns the number of keys in the new set.
        """
        args = list_or_args(keys, args)
        return await self.connection.execute('SDIFFSTORE', dest, *args)

    async def sismember(self, name, value):
        """
        Return a boolean indicating if ``value`` is a member of set ``name``
        """
        return await self.connection.execute('SISMEMBER', name, value)

    async def smembers(self, name):
        """
        Return all members of the set ``name``
        """
        return await self.connection.execute('SMEMBERS', name)

    async def smove(self, src, dst, value):
        """
        Move ``value`` from set ``src`` to set ``dst`` atomically
        """
        return await self.connection.execute('SMOVE', src, dst, value)

    async def spop(self, name, count=None):
        """
        Remove and return a random member of set ``name``
        """
        args = (count is not None) and [count] or []
        return await self.connection.execute('SPOP', name, *args)

    async def srandmember(self, name, number=None):
        """
        If ``number`` is None, returns a random member of set ``name``.

        If ``number`` is supplied, returns a list of ``number`` random
        members of set ``name``. Note this is only available when running
        Redis 2.6+.
        """
        args = (number is not None) and [number] or []
        return await self.connection.execute('SRANDMEMBER', name, *args)

    async def srem(self, name, *values):
        """
        Remove ``values`` from set ``name``
        """
        return await self.connection.execute('SREM', name, *values)

    async def sunion(self, keys, *args):
        """
        Return the union of sets specified by ``keys``
        """
        args = list_or_args(keys, args)
        return await self.connection.execute('SUNION', *args)

    async def sunionstore(self, dest, keys, *args):
        """
        Store the union of sets specified by ``keys`` into a new
        set named ``dest``.  Returns the number of keys in the new set.
        """
        args = list_or_args(keys, args)
        return await self.connection.execute('SUNIONSTORE', dest, *args)

    # STREAMS COMMANDS
    async def xack(self, name, groupname, *ids):
        """
        Acknowledges the successful processing of one or more messages.
        name: name of the stream.
        groupname: name of the consumer group.
        *ids: message ids to acknowlege.
        """
        return await self.connection.execute('XACK', name, groupname, *ids)

    async def xadd(self, name, fields, _id='*', maxlen=None, approximate=True):
        """
        Add to a stream.
        name: name of the stream
        fields: dict of field/value pairs to insert into the stream
        id: Location to insert this record. By default it is appended.
        maxlen: truncate old stream members beyond this size
        approximate: actual stream length may be slightly more than maxlen

        """
        pieces = []
        if maxlen is not None:
            if not isinstance(maxlen, int) or maxlen < 1:
                raise RedisError('XADD maxlen must be a positive integer')
            pieces.append(b'MAXLEN')
            if approximate:
                pieces.append(b'~')
            pieces.append(str(maxlen))
        pieces.append(_id)
        if not isinstance(fields, dict) or len(fields) == 0:
            raise RedisError('XADD fields must be a non-empty dict')
        for pair in iter(fields.items()):
            pieces.extend(pair)
        return await self.connection.execute('XADD', name, *pieces)

    async def xclaim(self, name, groupname, consumername, min_idle_time, message_ids,
                     idle=None, _time=None, retrycount=None, force=False,
                     justid=False):
        """
        Changes the ownership of a pending message.
        name: name of the stream.
        groupname: name of the consumer group.
        consumername: name of a consumer that claims the message.
        min_idle_time: filter messages that were idle less than this amount of
        milliseconds
        message_ids: non-empty list or tuple of message IDs to claim
        idle: optional. Set the idle time (last time it was delivered) of the
         message in ms
        time: optional integer. This is the same as idle but instead of a
         relative amount of milliseconds, it sets the idle time to a specific
         Unix time (in milliseconds).
        retrycount: optional integer. set the retry counter to the specified
         value. This counter is incremented every time a message is delivered
         again.
        force: optional boolean, false by default. Creates the pending message
         entry in the PEL even if certain specified IDs are not already in the
         PEL assigned to a different client.
        justid: optional boolean, false by default. Return just an array of IDs
         of messages successfully claimed, without returning the actual message
        """
        if not isinstance(min_idle_time, int) or min_idle_time < 0:
            raise RedisError("XCLAIM min_idle_time must be a non negative "
                             "integer")
        if not isinstance(message_ids, (list, tuple)) or not message_ids:
            raise RedisError("XCLAIM message_ids must be a non empty list or "
                             "tuple of message IDs to claim")

        kwargs = {}
        pieces = [name, groupname, consumername, str(min_idle_time)]
        pieces.extend(list(message_ids))

        if idle is not None:
            if not isinstance(idle, int):
                raise RedisError("XCLAIM idle must be an integer")
            pieces.extend((b'IDLE', str(idle)))
        if _time is not None:
            if not isinstance(_time, int):
                raise RedisError("XCLAIM time must be an integer")
            pieces.extend((b'TIME', str(_time)))
        if retrycount is not None:
            if not isinstance(retrycount, int):
                raise RedisError("XCLAIM retrycount must be an integer")
            pieces.extend((b'RETRYCOUNT', str(retrycount)))

        if force:
            if not isinstance(force, bool):
                raise RedisError("XCLAIM force must be a boolean")
            pieces.append(b'FORCE')
        if justid:
            if not isinstance(justid, bool):
                raise RedisError("XCLAIM justid must be a boolean")
            pieces.append(b'JUSTID')
            kwargs['parse_justid'] = True
        return await self.connection.execute('XCLAIM', *pieces, **kwargs)

    async def xdel(self, name, *ids):
        """
        Deletes one or more messages from a stream.
        name: name of the stream.
        *ids: message ids to delete.
        """
        return await self.connection.execute('XDEL', name, *ids)

    async def xgroup_create(self, name, groupname, _id='$', mkstream=False):
        """
        Create a new consumer group associated with a stream.
        name: name of the stream.
        groupname: name of the consumer group.
        id: ID of the last item in the stream to consider already delivered.
        """
        pieces = ['XGROUP CREATE', name, groupname, _id]
        if mkstream:
            pieces.append(b'MKSTREAM')
        return await self.connection.execute(*pieces)

    async def xgroup_delconsumer(self, name, groupname, consumername):
        """
        Remove a specific consumer from a consumer group.
        Returns the number of pending messages that the consumer had before it
        was deleted.
        name: name of the stream.
        groupname: name of the consumer group.
        consumername: name of consumer to delete
        """
        return await self.connection.execute('XGROUP DELCONSUMER', name, groupname,
                                             consumername)

    async def xgroup_destroy(self, name, groupname):
        """
        Destroy a consumer group.
        name: name of the stream.
        groupname: name of the consumer group.
        """
        return await self.connection.execute('XGROUP DESTROY', name, groupname)

    async def xgroup_setid(self, name, groupname, _id):
        """
        Set the consumer group last delivered ID to something else.
        name: name of the stream.
        groupname: name of the consumer group.
        id: ID of the last item in the stream to consider already delivered.
        """
        return await self.connection.execute('XGROUP SETID', name, groupname, _id)

    async def xinfo_consumers(self, name, groupname):
        """
        Returns general information about the consumers in the group.
        name: name of the stream.
        groupname: name of the consumer group.
        """
        return await self.connection.execute('XINFO CONSUMERS', name, groupname)

    async def xinfo_groups(self, name):
        """
        Returns general information about the consumer groups of the stream.
        name: name of the stream.
        """
        return await self.connection.execute('XINFO GROUPS', name)

    async def xinfo_stream(self, name):
        """
        Returns general information about the stream.
        name: name of the stream.
        """
        return await self.connection.execute('XINFO STREAM', name)

    async def xlen(self, name):
        """
        Returns the number of elements in a given stream.
        """
        return await self.connection.execute('XLEN', name)

    async def xpending(self, name, groupname):
        """
        Returns information about pending messages of a group.
        name: name of the stream.
        groupname: name of the consumer group.
        """
        return await self.connection.execute('XPENDING', name, groupname)

    async def xrange(self, name, _min='-', _max='+', count=None):
        """
        Read stream values within an interval.
        name: name of the stream.
        start: first stream ID. defaults to '-',
               meaning the earliest available.
        finish: last stream ID. defaults to '+',
                meaning the latest available.
        count: if set, only return this many items, beginning with the
               earliest available.
        """
        pieces = [_min, _max]
        if count is not None:
            if not isinstance(count, int) or count < 1:
                raise RedisError('XRANGE count must be a positive integer')
            pieces.append(b'COUNT')
            pieces.append(str(count))

        return await self.connection.execute('XRANGE', name, *pieces)

    async def xread(self, streams, count=None, block=None):
        """
        Block and monitor multiple streams for new data.
        streams: a dict of stream names to stream IDs, where
                   IDs indicate the last ID already seen.
        count: if set, only return this many items, beginning with the
               earliest available.
        block: number of milliseconds to wait, if nothing already present.
        """
        pieces = []
        if block is not None:
            if not isinstance(block, int) or block < 0:
                raise RedisError('XREAD block must be a non-negative integer')
            pieces.append(b'BLOCK')
            pieces.append(str(block))
        if count is not None:
            if not isinstance(count, int) or count < 1:
                raise RedisError('XREAD count must be a positive integer')
            pieces.append(b'COUNT')
            pieces.append(str(count))
        if not isinstance(streams, dict) or len(streams) == 0:
            raise RedisError('XREAD streams must be a non empty dict')
        pieces.append(b'STREAMS')
        keys, values = zip(*iter(streams.items()))
        pieces.extend(keys)
        pieces.extend(values)
        return await self.connection.execute('XREAD', *pieces)

    async def xreadgroup(self, groupname, consumername, streams, count=None,
                         block=None, noack=False):
        """
        Read from a stream via a consumer group.
        groupname: name of the consumer group.
        consumername: name of the requesting consumer.
        streams: a dict of stream names to stream IDs, where
               IDs indicate the last ID already seen.
        count: if set, only return this many items, beginning with the
               earliest available.
        block: number of milliseconds to wait, if nothing already present.
        noack: do not add messages to the PEL
        """
        pieces = [b'GROUP', groupname, consumername]
        if count is not None:
            if not isinstance(count, int) or count < 1:
                raise RedisError("XREADGROUP count must be a positive integer")
            pieces.append(b'COUNT')
            pieces.append(str(count))
        if block is not None:
            if not isinstance(block, int) or block < 0:
                raise RedisError("XREADGROUP block must be a non-negative "
                                 "integer")
            pieces.append(b'BLOCK')
            pieces.append(str(block))
        if noack:
            pieces.append(b'NOACK')
        if not isinstance(streams, dict) or len(streams) == 0:
            raise RedisError('XREADGROUP streams must be a non empty dict')
        pieces.append(b'STREAMS')
        pieces.extend(streams.keys())
        pieces.extend(streams.values())
        return await self.connection.execute('XREADGROUP', *pieces)

    async def xrevrange(self, name, _max='+', _min='-', count=None):
        """
        Read stream values within an interval, in reverse order.
        name: name of the stream
        start: first stream ID. defaults to '+',
               meaning the latest available.
        finish: last stream ID. defaults to '-',
                meaning the earliest available.
        count: if set, only return this many items, beginning with the
               latest available.
        """
        pieces = [_max, _min]
        if count is not None:
            if not isinstance(count, int) or count < 1:
                raise RedisError('XREVRANGE count must be a positive integer')
            pieces.append(b'COUNT')
            pieces.append(str(count))

        return await self.connection.execute('XREVRANGE', name, *pieces)

    async def xtrim(self, name, maxlen, approximate=True):
        """
        Trims old messages from a stream.
        name: name of the stream.
        maxlen: truncate old stream messages beyond this size
        approximate: actual stream length may be slightly more than maxlen
        """
        pieces = [b'MAXLEN']
        if approximate:
            pieces.append(b'~')
        pieces.append(maxlen)
        return await self.connection.execute('XTRIM', name, *pieces)

    # SORTED SET COMMANDS
    async def zadd(self, name, mapping, nx=False, xx=False, ch=False, incr=False):
        """
        Set any number of element-name, score pairs to the key ``name``. Pairs
        are specified as a dict of element-names keys to score values.

        ``nx`` forces ZADD to only create new elements and not to update
        scores for elements that already exist.

        ``xx`` forces ZADD to only update scores of elements that already
        exist. New elements will not be added.

        ``ch`` modifies the return value to be the numbers of elements changed.
        Changed elements include new elements that were added and elements
        whose scores changed.

        ``incr`` modifies ZADD to behave like ZINCRBY. In this mode only a
        single element/score pair can be specified and the score is the amount
        the existing score will be incremented by. When using this mode the
        return value of ZADD will be the new score of the element.

        The return value of ZADD varies based on the mode specified. With no
        options, ZADD returns the number of new elements added to the sorted
        set.
        """
        if not mapping:
            raise RedisError("ZADD requires at least one element/score pair")
        if nx and xx:
            raise RedisError("ZADD allows either 'nx' or 'xx', not both")
        if incr and len(mapping) != 1:
            raise RedisError("ZADD option 'incr' only works when passing a "
                             "single element/score pair")
        pieces = []
        options = {}
        if nx:
            pieces.append(b'NX')
        if xx:
            pieces.append(b'XX')
        if ch:
            pieces.append(b'CH')
        if incr:
            pieces.append(b'INCR')
            options['as_score'] = True
        for pair in iter(mapping.items()):
            pieces.append(pair[1])
            pieces.append(pair[0])
        return await self.connection.execute('ZADD', name, *pieces, **options)

    async def zcard(self, name):
        """
        Return the number of elements in the sorted set ``name``
        """
        return await self.connection.execute('ZCARD', name)

    async def zcount(self, name, _min, _max):
        """
        Returns the number of elements in the sorted set at key ``name`` with
        a score between ``min`` and ``max``.
        """
        return await self.connection.execute('ZCOUNT', name, _min, _max)

    async def zincrby(self, name, amount, value):
        """
        Increment the score of ``value`` in sorted set ``name`` by ``amount``
        """
        return await self.connection.execute('ZINCRBY', name, amount, value)

    async def zlexcount(self, name, _min, _max):
        """
        Return the number of items in the sorted set ``name`` between the
        lexicographical range ``min`` and ``max``.
        """
        return await self.connection.execute('ZLEXCOUNT', name, _min, _max)

    async def zpopmax(self, name, count=None):
        """
        Remove and return up to ``count`` members with the highest scores
        from the sorted set ``name``.
        """
        args = (count is not None) and [count] or []
        options = {
            'withscores': True
        }
        return await self.connection.execute('ZPOPMAX', name, *args, **options)

    async def zpopmin(self, name, count=None):
        """
        Remove and return up to ``count`` members with the lowest scores
        from the sorted set ``name``.
        """
        args = (count is not None) and [count] or []
        options = {
            'withscores': True
        }
        return await self.connection.execute('ZPOPMIN', name, *args, **options)

    async def bzpopmax(self, keys, timeout=0):
        """
        ZPOPMAX a value off of the first non-empty sorted set
        named in the ``keys`` list.

        If none of the sorted sets in ``keys`` has a value to ZPOPMAX,
        then block for ``timeout`` seconds, or until a member gets added
        to one of the sorted sets.

        If timeout is 0, then block indefinitely.
        """
        if timeout is None:
            timeout = 0
        keys = list_or_args(keys, None)
        keys.append(timeout)
        return await self.connection.execute('BZPOPMAX', *keys)

    async def bzpopmin(self, keys, timeout=0):
        """
        ZPOPMIN a value off of the first non-empty sorted set
        named in the ``keys`` list.

        If none of the sorted sets in ``keys`` has a value to ZPOPMIN,
        then block for ``timeout`` seconds, or until a member gets added
        to one of the sorted sets.

        If timeout is 0, then block indefinitely.
        """
        if timeout is None:
            timeout = 0
        keys = list_or_args(keys, None)
        keys.append(timeout)
        return await self.connection.execute('BZPOPMIN', *keys)

    async def zrange(self, name, start, end, desc=False, withscores=False,
                     score_cast_func=float):
        """
        Return a range of values from sorted set ``name`` between
        ``start`` and ``end`` sorted in ascending order.

        ``start`` and ``end`` can be negative, indicating the end of the range.

        ``desc`` a boolean indicating whether to sort the results descendingly

        ``withscores`` indicates to return the scores along with the values.
        The return type is a list of (value, score) pairs

        ``score_cast_func`` a callable used to cast the score return value
        """
        if desc:
            return self.zrevrange(name, start, end, withscores,
                                  score_cast_func)
        pieces = ['ZRANGE', name, start, end]
        if withscores:
            pieces.append(b'WITHSCORES')
        options = {
            'withscores': withscores,
            'score_cast_func': score_cast_func
        }
        return await self.connection.execute(*pieces, **options)

    async def zrangebylex(self, name, _min, _max, start=None, num=None):
        """
        Return the lexicographical range of values from sorted set ``name``
        between ``min`` and ``max``.

        If ``start`` and ``num`` are specified, then return a slice of the
        range.
        """
        if (start is not None and num is None) or \
                (num is not None and start is None):
            raise RedisError("``start`` and ``num`` must both be specified")
        pieces = ['ZRANGEBYLEX', name, _min, _max]
        if start is not None and num is not None:
            pieces.extend([b'LIMIT', start, num])
        return await self.connection.execute(*pieces)

    async def zrevrangebylex(self, name, _max, _min, start=None, num=None):
        """
        Return the reversed lexicographical range of values from sorted set
        ``name`` between ``max`` and ``min``.

        If ``start`` and ``num`` are specified, then return a slice of the
        range.
        """
        if (start is not None and num is None) or \
                (num is not None and start is None):
            raise RedisError("``start`` and ``num`` must both be specified")
        pieces = ['ZREVRANGEBYLEX', name, _max, _min]
        if start is not None and num is not None:
            pieces.extend([b'LIMIT', start, num])
        return await self.connection.execute(*pieces)

    async def zrangebyscore(self, name, _min, _max, start=None, num=None,
                            withscores=False, score_cast_func=float):
        """
        Return a range of values from the sorted set ``name`` with scores
        between ``min`` and ``max``.

        If ``start`` and ``num`` are specified, then return a slice
        of the range.

        ``withscores`` indicates to return the scores along with the values.
        The return type is a list of (value, score) pairs

        `score_cast_func`` a callable used to cast the score return value
        """
        if (start is not None and num is None) or \
                (num is not None and start is None):
            raise RedisError("``start`` and ``num`` must both be specified")
        pieces = ['ZRANGEBYSCORE', name, _min, _max]
        if start is not None and num is not None:
            pieces.extend([b'LIMIT', start, num])
        if withscores:
            pieces.append(b'WITHSCORES')
        options = {
            'withscores': withscores,
            'score_cast_func': score_cast_func
        }
        return await self.connection.execute(*pieces, **options)

    async def zrank(self, name, value):
        """
        Returns a 0-based value indicating the rank of ``value`` in sorted set
        ``name``
        """
        return await self.connection.execute('ZRANK', name, value)

    async def zrem(self, name, *values):
        """
        Remove member ``values`` from sorted set ``name``
        """
        return await self.connection.execute('ZREM', name, *values)

    async def zremrangebylex(self, name, _min, _max):
        """
        Remove all elements in the sorted set ``name`` between the
        lexicographical range specified by ``min`` and ``max``.

        Returns the number of elements removed.
        """
        return await self.connection.execute('ZREMRANGEBYLEX', name, _min, _max)

    async def zremrangebyrank(self, name, _min, _max):
        """
        Remove all elements in the sorted set ``name`` with ranks between
        ``min`` and ``max``. Values are 0-based, ordered from smallest score
        to largest. Values can be negative indicating the highest scores.
        Returns the number of elements removed
        """
        return await self.connection.execute('ZREMRANGEBYRANK', name, _min, _max)

    async def zremrangebyscore(self, name, _min, _max):
        """
        Remove all elements in the sorted set ``name`` with scores
        between ``min`` and ``max``. Returns the number of elements removed.
        """
        return await self.connection.execute('ZREMRANGEBYSCORE', name, _min, _max)

    async def zrevrange(self, name, start, end, withscores=False,
                        score_cast_func=float):
        """
        Return a range of values from sorted set ``name`` between
        ``start`` and ``end`` sorted in descending order.

        ``start`` and ``end`` can be negative, indicating the end of the range.

        ``withscores`` indicates to return the scores along with the values
        The return type is a list of (value, score) pairs

        ``score_cast_func`` a callable used to cast the score return value
        """
        pieces = ['ZREVRANGE', name, start, end]
        if withscores:
            pieces.append(b'WITHSCORES')
        options = {
            'withscores': withscores,
            'score_cast_func': score_cast_func
        }
        return await self.connection.execute(*pieces, **options)

    async def zrevrangebyscore(self, name, _max, _min, start=None, num=None,
                               withscores=False, score_cast_func=float):
        """
        Return a range of values from the sorted set ``name`` with scores
        between ``min`` and ``max`` in descending order.

        If ``start`` and ``num`` are specified, then return a slice
        of the range.

        ``withscores`` indicates to return the scores along with the values.
        The return type is a list of (value, score) pairs

        ``score_cast_func`` a callable used to cast the score return value
        """
        if (start is not None and num is None) or \
                (num is not None and start is None):
            raise RedisError("``start`` and ``num`` must both be specified")
        pieces = ['ZREVRANGEBYSCORE', name, _max, _min]
        if start is not None and num is not None:
            pieces.extend([b'LIMIT', start, num])
        if withscores:
            pieces.append(b'WITHSCORES')
        options = {
            'withscores': withscores,
            'score_cast_func': score_cast_func
        }
        return await self.connection.execute(*pieces, **options)

    async def zrevrank(self, name, value):
        """
        Returns a 0-based value indicating the descending rank of
        ``value`` in sorted set ``name``
        """
        return await self.connection.execute('ZREVRANK', name, value)

    async def zscore(self, name, value):
        """
        Return the score of element ``value`` in sorted set ``name``
        """
        return await self.connection.execute('ZSCORE', name, value)

    # HYPERLOGLOG COMMANDS
    async def pfadd(self, name, *values):
        """
        Adds the specified elements to the specified HyperLogLog.
        """
        return await self.connection.execute('PFADD', name, *values)

    async def pfcount(self, *sources):
        """
        Return the approximated cardinality of
        the set observed by the HyperLogLog at key(s).
        """
        return await self.connection.execute('PFCOUNT', *sources)

    async def pfmerge(self, dest, *sources):
        """
        Merge N different HyperLogLogs into a single one.
        """
        return await self.connection.execute('PFMERGE', dest, *sources)

    # HASH COMMANDS
    async def hdel(self, name, *keys):
        """
        Delete ``keys`` from hash ``name``
        """
        return await self.connection.execute('HDEL', name, *keys)

    async def hexists(self, name, key):
        """
        Returns a boolean indicating if ``key`` exists within hash ``name``
        """
        return await self.connection.execute('HEXISTS', name, key)

    async def hget(self, name, key):
        """
        Return the value of ``key`` within the hash ``name``
        """
        return await self.connection.execute('HGET', name, key)

    async def hgetall(self, name):
        """
        Return a Python dict of the hash's name/value pairs
        """
        return await self.connection.execute('HGETALL', name)

    async def hincrby(self, name, key, amount=1):
        """
        Increment the value of ``key`` in hash ``name`` by ``amount``
        """
        return await self.connection.execute('HINCRBY', name, key, amount)

    async def hincrbyfloat(self, name, key, amount=1.0):
        """
        Increment the value of ``key`` in hash ``name`` by floating ``amount``
        """
        return await self.connection.execute('HINCRBYFLOAT', name, key, amount)

    async def hkeys(self, name):
        """
        Return the list of keys within hash ``name``
        """
        return await self.connection.execute('HKEYS', name)

    async def hlen(self, name):
        """
        Return the number of elements in hash ``name``
        """
        return await self.connection.execute('HLEN', name)

    async def hset(self, name, key=None, value=None, mapping=None):
        """
        Set ``key`` to ``value`` within hash ``name``,
        ``mapping`` accepts a dict of key/value pairs that that will be
        added to hash ``name``.
        Returns the number of fields that were added.
        """
        if key is None and not mapping:
            raise RedisError("'hset' with no key value pairs")
        items = []
        if key is not None:
            items.extend((key, value))
        if mapping:
            for pair in mapping.items():
                items.extend(pair)

        return await self.connection.execute('HSET', name, *items)

    async def hsetnx(self, name, key, value):
        """
        Set ``key`` to ``value`` within hash ``name`` if ``key`` does not
        exist.  Returns 1 if HSETNX created a field, otherwise 0.
        """
        return await self.connection.execute('HSETNX', name, key, value)

    async def hmget(self, name, keys, *args):
        """
        Returns a list of values ordered identically to ``keys``
        """
        args = list_or_args(keys, args)
        return await self.connection.execute('HMGET', name, *args)

    async def hvals(self, name):
        """
        Return the list of values within hash ``name``
        """
        return await self.connection.execute('HVALS', name)

    async def hstrlen(self, name, key):
        """
        Return the number of bytes stored in the value of ``key``
        within hash ``name``
        """
        return await self.connection.execute('HSTRLEN', name, key)

    async def publish(self, channel, message):
        """
        Publish ``message`` on ``channel``.
        Returns the number of subscribers the message was delivered to.
        """
        return await self.connection.execute('PUBLISH', channel, message)

    async def pubsub_channels(self, pattern='*'):
        """
        Return a list of channels that have at least one subscriber
        """
        return await self.connection.execute('PUBSUB CHANNELS', pattern)

    async def pubsub_numpat(self):
        """
        Returns the number of subscriptions to patterns
        """
        return await self.connection.execute('PUBSUB NUMPAT')

    async def pubsub_numsub(self, *args):
        """
        Return a list of (channel, number of subscribers) tuples
        for each channel given in ``*args``
        """
        return await self.connection.execute('PUBSUB NUMSUB', *args)

    async def cluster(self, cluster_arg, *args):
        return await self.connection.execute('CLUSTER %s' % cluster_arg.upper(), *args)

    async def eval(self, script, numkeys, *keys_and_args):
        """
        Execute the Lua ``script``, specifying the ``numkeys`` the script
        will touch and the key names and argument values in ``keys_and_args``.
        Returns the result of the script.

        In practice, use the object returned by ``register_script``. This
        function exists purely for Redis API completion.
        """
        return await self.connection.execute('EVAL', script, numkeys, *keys_and_args)

    async def evalsha(self, sha, numkeys, *keys_and_args):
        """
        Use the ``sha`` to execute a Lua script already registered via EVAL
        or SCRIPT LOAD. Specify the ``numkeys`` the script will touch and the
        key names and argument values in ``keys_and_args``. Returns the result
        of the script.

        In practice, use the object returned by ``register_script``. This
        function exists purely for Redis API completion.
        """
        return await self.connection.execute('EVALSHA', sha, numkeys, *keys_and_args)

    async def script_exists(self, *args):
        """
        Check if a script exists in the script cache by specifying the SHAs of
        each script as ``args``. Returns a list of boolean values indicating if
        if each already script exists in the cache.
        """
        return await self.connection.execute('SCRIPT EXISTS', *args)

    async def script_flush(self):
        """
        Flush all scripts from the script cache
        """
        return await self.connection.execute('SCRIPT FLUSH')

    async def script_kill(self):
        """
        Kill the currently executing Lua script
        """
        return await self.connection.execute('SCRIPT KILL')

    async def script_load(self, script):
        """
        Load a Lua ``script`` into the script cache. Returns the SHA.
        """
        return await self.connection.execute('SCRIPT LOAD', script)

    # GEO COMMANDS
    async def geoadd(self, name, *values):
        """
        Add the specified geospatial items to the specified key identified
        by the ``name`` argument. The Geospatial items are given as ordered
        members of the ``values`` argument, each item or place is formed by
        the triad longitude, latitude and name.
        """
        if len(values) % 3 != 0:
            raise RedisError("GEOADD requires places with lon, lat and name"
                             " values")
        return await self.connection.execute('GEOADD', name, *values)

    async def geodist(self, name, place1, place2, unit=None):
        """
        Return the distance between ``place1`` and ``place2`` members of the
        ``name`` key.
        The units must be one of the following : m, km mi, ft. By default
        meters are used.
        """
        pieces = [name, place1, place2]
        if unit and unit not in ('m', 'km', 'mi', 'ft'):
            raise RedisError("GEODIST invalid unit")
        elif unit:
            pieces.append(unit)
        return await self.connection.execute('GEODIST', *pieces)

    async def geohash(self, name, *values):
        """
        Return the geo hash string for each item of ``values`` members of
        the specified key identified by the ``name`` argument.
        """
        return await self.connection.execute('GEOHASH', name, *values)

    async def geopos(self, name, *values):
        """
        Return the positions of each item of ``values`` as members of
        the specified key identified by the ``name`` argument. Each position
        is represented by the pairs lon and lat.
        """
        return await self.connection.execute('GEOPOS', name, *values)

    async def georadius(self, name, longitude, latitude, radius, unit=None,
                        withdist=False, withcoord=False, withhash=False, count=None,
                        sort=None, store=None, store_dist=None):
        """
        Return the members of the specified key identified by the
        ``name`` argument which are within the borders of the area specified
        with the ``latitude`` and ``longitude`` location and the maximum
        distance from the center specified by the ``radius`` value.

        The units must be one of the following : m, km mi, ft. By default

        ``withdist`` indicates to return the distances of each place.

        ``withcoord`` indicates to return the latitude and longitude of
        each place.

        ``withhash`` indicates to return the geohash string of each place.

        ``count`` indicates to return the number of elements up to N.

        ``sort`` indicates to return the places in a sorted way, ASC for
        nearest to fairest and DESC for fairest to nearest.

        ``store`` indicates to save the places names in a sorted set named
        with a specific key, each element of the destination sorted set is
        populated with the score got from the original geo sorted set.

        ``store_dist`` indicates to save the places names in a sorted set
        named with a specific key, instead of ``store`` the sorted set
        destination score is set with the distance.
        """
        return self._georadiusgeneric('GEORADIUS',
                                      name, longitude, latitude, radius,
                                      unit=unit, withdist=withdist,
                                      withcoord=withcoord, withhash=withhash,
                                      count=count, sort=sort, store=store,
                                      store_dist=store_dist)

    async def georadiusbymember(self, name, member, radius, unit=None,
                                withdist=False, withcoord=False, withhash=False,
                                count=None, sort=None, store=None, store_dist=None):
        """
        This command is exactly like ``georadius`` with the sole difference
        that instead of taking, as the center of the area to query, a longitude
        and latitude value, it takes the name of a member already existing
        inside the geospatial index represented by the sorted set.
        """
        return self._georadiusgeneric('GEORADIUSBYMEMBER',
                                      name, member, radius, unit=unit,
                                      withdist=withdist, withcoord=withcoord,
                                      withhash=withhash, count=count,
                                      sort=sort, store=store,
                                      store_dist=store_dist)

    async def _georadiusgeneric(self, command, *args, **kwargs):
        pieces = list(args)
        if kwargs['unit'] and kwargs['unit'] not in ('m', 'km', 'mi', 'ft'):
            raise RedisError("GEORADIUS invalid unit")
        elif kwargs['unit']:
            pieces.append(kwargs['unit'])
        else:
            pieces.append('m', )

        for arg_name, byte_repr in (
                ('withdist', b'WITHDIST'),
                ('withcoord', b'WITHCOORD'),
                ('withhash', b'WITHHASH')):
            if kwargs[arg_name]:
                pieces.append(byte_repr)

        if kwargs['count']:
            pieces.extend([b'COUNT', kwargs['count']])

        if kwargs['sort']:
            if kwargs['sort'] == 'ASC':
                pieces.append(b'ASC')
            elif kwargs['sort'] == 'DESC':
                pieces.append(b'DESC')
            else:
                raise RedisError("GEORADIUS invalid sort")

        if kwargs['store'] and kwargs['store_dist']:
            raise RedisError("GEORADIUS store and store_dist cant be set"
                             " together")

        if kwargs['store']:
            pieces.extend([b'STORE', kwargs['store']])

        if kwargs['store_dist']:
            pieces.extend([b'STOREDIST', kwargs['store_dist']])

        return await self.connection.execute(command, *pieces, **kwargs)
