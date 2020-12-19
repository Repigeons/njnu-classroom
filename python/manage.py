#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/5 0005
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  manage.py
""""""
import os

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-r', '--run', default=None, type=str, help="run the service module")
    parser.add_argument('-c', '--conf', default=None, type=str, help="set the config directory, default 'conf/'")
    args = parser.parse_args()

    if args.run is not None:
        from importlib import import_module

        os.environ['conf'] = 'conf' if args.conf is None else args.conf

        try:
            getattr(import_module(f"App.{args.run}.__main__"), 'main')()
        except ModuleNotFoundError as e:
            if e.name == f"App.{args.run}":
                print(f"No module named '{args.run}'")
            else:
                raise e
        except AttributeError as e:
            if str(e) == f"module 'App.{args.run}.__main__' has no attribute 'main'":
                print(e)
            else:
                raise e
