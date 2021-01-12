#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/5 0005
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  manage.py
""""""
from logging.handlers import TimedRotatingFileHandler
import logging
import os
import time
from argparse import ArgumentParser, Namespace

os.environ["startup_time"] = str(int(time.time() * 1000))


def __init__logging(filename: str) -> None:
    # 基础配置
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s]\t"
               "[ %(levelname)s ]\t\t"
               "[\t%(module)20s\t]\t\t"
               ": %(message)s"
    )
    # 日志文件
    if filename:
        # get logging file
        filename = os.path.abspath(os.path.join("/var/log/NjnuClassroom", filename))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # set logger configuration
        logger = logging.getLogger()
        formatter = logger.handlers[0].formatter
        handler = TimedRotatingFileHandler(filename=filename, encoding="utf8", when='D', backupCount=10)
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def main(args: Namespace):
    __init__logging(args.log)

    logging.info("Starting Application with PID [%d]", os.getpid())

    if args.run:
        os.environ['application.yml'] = os.getenv("application.yml", "resources/application.yml")
        if not os.path.exists(os.getenv("application.yml")):
            logging.error("FileNotFoundError: No such file [%s]", os.getenv("application.yml"))
            exit(-1)

        try:
            logging.info("Initializing module [%s]", args.run)
            module = __import__(f"App.{args.run}.__main__", fromlist=("App", args.run, "__main__"))
        except ModuleNotFoundError as e:
            if e.name == f"App.{args.run}":
                logging.error("ModuleNotFoundError: No such module [%s]", args.run)
                exit(-1)
            raise e

        logging.info("Starting Service [%s]", args.run)
        module.main()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-r', '--run', type=str, help="Service module")
    parser.add_argument('-l', '--log', type=str, help="Logging file")
    main(args=parser.parse_args())
