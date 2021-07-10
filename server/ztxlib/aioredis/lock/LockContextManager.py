#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aioredis import ConnectionsPool

from .Lock import Lock as _Lock


def lock(
        pool: ConnectionsPool,
        name: str,
        wait_timeout: int = -1,
        timeout: int = 0
):
    return LockContextManager(
        pool=pool,
        name=name,
        wait_timeout=wait_timeout,
        timeout=timeout
    )


class LockContextManager:
    def __init__(self, **kwargs):
        self.lock = _Lock(kwargs['pool'])
        self.name = kwargs['name']
        self.wait_timeout = kwargs['wait_timeout']
        self.timeout = kwargs['timeout']

    async def __aenter__(self):
        if await self.lock.acquire(
                name=self.name,
                wait_timeout=self.wait_timeout,
                timeout=self.timeout
        ):
            return Lock(self.lock)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.lock.release()


class Lock:
    def __init__(self, _lock):
        self._lock = _lock

    async def extend(self, timeout):
        await self._lock.extend(timeout)
