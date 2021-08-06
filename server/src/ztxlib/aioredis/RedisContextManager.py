#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aioredis import ConnectionsPool

from .Redis import Redis


class RedisContextManager:
    @classmethod
    def start(cls, pool: ConnectionsPool) -> 'RedisContextManager':
        """
        创建Redis上下文管理器

        :param pool: Redis 连接池
        :return:
        """
        return cls(pool)

    def __init__(self, pool: ConnectionsPool):
        self.pool = pool

    async def __aenter__(self) -> Redis:
        self._context = self.pool.get()
        connection = await self._context.__aenter__()
        self._redis = Redis(connection)
        return self._redis

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._redis.close()
        await self._context.__aexit__(exc_type, exc_val, exc_tb)
        del self._redis
        del self._context
