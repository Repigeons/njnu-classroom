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

    if args.run is None:
        pass

    elif args.run == "Spider":
        from App.Spider.__main__ import main

        main()

    elif args.run == "Server":
        from App.Server.__main__ import main

        main()

    elif args.run == "Notice":
        from App.Notice.__main__ import main

        main()

    else:
        print(f"Unresolved module `{args.run}`")
