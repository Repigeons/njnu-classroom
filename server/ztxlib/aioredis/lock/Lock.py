#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio
import logging
import time
import uuid
from logging import Logger

from aioredis import ConnectionsPool

from . import lua_scripts
from .ScriptingCommandsMixin import ScriptingCommandsMixin
from ..exceptions import UnlockError, WaitingTimeoutError


class Lock:
    logger: Logger = logging.getLogger("RedisLock")

    def __init__(self, pool: ConnectionsPool):
        self.name = None
        self.uuid = str(uuid.uuid4())
        self.scripting = ScriptingCommandsMixin(pool)

    async def acquire(self,
                      name: str,
                      wait_timeout: int = -1,
                      timeout: int = 0
                      ):
        await lua_scripts.initialize(script_load=self.scripting.script_load)
        self.name = "lock:%s" % name
        start_time = time.time()
        while True:
            if await self._acquire(timeout):
                Lock.logger.info("Acquired RedisLock [%s]", self.name)
                return True
            if 0 <= wait_timeout < time.time() - start_time:
                raise WaitingTimeoutError("Timeout while waiting for RedisLock [%s]" % self.name)
            await asyncio.sleep(0.01)

    async def release(self):
        if await self.scripting.eval_sha(
                lua_scripts.RELEASE,
                keys=[self.name],
                args=[self.uuid]
        ):
            Lock.logger.info("Released RedisLock [%s]", self.name)
            return True
        raise UnlockError

    async def extend(self, timeout: int):
        await self.scripting.eval_sha(
            lua_scripts.EXTEND,
            keys=[self.name],
            args=[self.uuid, timeout * 1000]
        )

    async def renew(self, timeout: int):
        await self.scripting.eval_sha(
            lua_scripts.RENEW,
            keys=[self.name],
            args=[self.uuid, timeout * 1000]
        )

    async def _acquire(self, timeout: int = 0):
        if timeout:
            return await self.scripting.eval_sha(
                lua_scripts.ACQUIRE,
                keys=[self.name],
                args=[self.uuid, timeout * 1000]
            )
        return await self.scripting.eval_sha(
            lua_scripts.ACQUIRE_WITHOUT_EXPIRE,
            keys=[self.name],
            args=[self.uuid]
        )
