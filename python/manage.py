#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/5 0005
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  manage.py
""""""
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-run', '--run', default=None, type=str)
    args = parser.parse_args()

    if args.run is not None:
        from importlib import import_module

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
