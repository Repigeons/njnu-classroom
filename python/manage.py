#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/5 0005
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  manage.py
""""""
import logging
import os
import time
from argparse import ArgumentParser, Namespace

os.environ['start_time'] = str(int(time.time() * 1000))

logging.basicConfig(
    level=logging.DEBUG if os.getenv("env") == "dev" else logging.INFO,
    # datefmt="%x %X",
    format="[%(asctime)s]\t"
           "[ %(levelname)s ]\t\t"
           "[ %(module)24s\t]\t\t"
           ": %(message)s",
)


def main(args: Namespace):
    if args.log is not None:
        logging.basicConfig(
            filemode='a',
            filename=args.log,
        )

    logging.info("Starting Application with PID %d", os.getpid())

    if args.run is not None:
        os.environ['application.yml'] = os.getenv("application.yml", "resources/application.yml")
        if not os.path.exists(os.getenv('application.yml')):
            logging.error("FileNotFoundError: No such file [%s]", os.getenv('application.yml'))
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
