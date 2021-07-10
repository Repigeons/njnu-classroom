#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aioredis import ConnectionsPool
from aioredis.util import wait_ok


class ScriptingCommandsMixin:
    def __init__(self, pool: ConnectionsPool):
        self.pool = pool

    async def eval_script(self, script: str, keys: list = None, args: list = None):
        """Execute a Lua script server side."""
        keys = [] if keys is None else keys
        args = [] if args is None else args
        async with self.pool.get() as redis:
            return await redis.execute(b'EVAL', script, len(keys), *(keys + args))

    async def eval_sha(self, digest: str, keys: list = None, args: list = None):
        """Execute a Lua script server side by its SHA1 digest."""
        keys = [] if keys is None else keys
        args = [] if args is None else args
        async with self.pool.get() as redis:
            return await redis.execute(b'EVALSHA', digest, len(keys), *(keys + args))

    async def script_exists(self, digest, *digests):
        """Check existence of scripts in the script cache."""
        async with self.pool.get() as redis:
            return await redis.execute(b'SCRIPT', b'EXISTS', digest, *digests)

    async def script_kill(self):
        """Kill the script currently in execution."""
        async with self.pool.get() as redis:
            fut = await redis.execute(b'SCRIPT', b'KILL')
            return wait_ok(fut)

    async def script_flush(self):
        """Remove all the scripts from the script cache."""
        async with self.pool.get() as redis:
            fut = await redis.execute(b"SCRIPT", b"FLUSH")
            return wait_ok(fut)

    async def script_load(self, script):
        """Load the specified Lua script into the script cache."""
        async with self.pool.get() as redis:
            return await redis.execute(b"SCRIPT", b"LOAD", script)
