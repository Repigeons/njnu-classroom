#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio
import logging
import os
import time
from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler

import aiofiles

from app import app, initialize, finalize

os.environ["startup_time"] = str(int(time.time() * 1000))


async def initialize_log(log_level: str):
    level = logging.getLevelName(str(log_level).upper())
    level = level if isinstance(level, int) else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] "
               "[ %(levelname)8s ] "
               "[ %(module)16s ] "
               ": %(message)s"
    )


async def initialize_logfile(logfile: str):
    # get logging file
    logfile = os.path.abspath(logfile)
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    async with aiofiles.open(logfile, 'a') as f:
        await f.write('\n')
    # set logger configuration
    logger = logging.getLogger()
    formatter = logger.handlers[0].formatter
    handler = TimedRotatingFileHandler(filename=logfile, encoding="UTF-8", when='D', backupCount=10)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main(module: str, log_level: str = None):
    loop = asyncio.get_event_loop()
    # 初始化
    loop.run_until_complete(
        asyncio.gather(
            initialize_log(log_level),
            initialize(),
        )
    )

    # 启动模块
    logging.info("Starting Application with PID [%d]", os.getpid())
    try:
        logging.info("Initializing module [%s]", module)
        starter = __import__(f"modules.{module}", fromlist=("modules", module))
        config = app['config']['application'][module]
        if 'log' in config and config['log']:
            loop.run_until_complete(initialize_logfile(logfile=config['log']))
        logging.info("Starting service [%s]", module)
        starter.main()

    except ModuleNotFoundError as e:
        if e.name == f"modules.{module}":
            logging.critical("ModuleNotFoundError: No such module [%s]", module)
            logging.info("Exit with code %d", -1)
            exit(-1)
        raise e
    finally:
        try:
            loop.run_until_complete(finalize())
        except RuntimeError:
            pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-r', '--run', type=str, help="Service module")
    parser.add_argument('-l', '--log', type=str, help="Logging level")
    args = parser.parse_args()
    if isinstance(args.run, str):
        main(
            module=args.run,
            log_level=args.log
        )
