#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/01/10
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _threading
""""""
from threading import Thread


class Threading:
    class __Thread(Thread):
        def __init__(self, function, **kwargs):
            super().__init__()
            self.__function = function
            self.__kwargs = kwargs

        def run(self):
            self.__function(**self.__kwargs)

    def __init__(self, method) -> 'Initialize threads with a method':
        self.__method = method
        self.__threads = []

    def start(self, thread_count: int = 1, **kwargs) -> None:
        """
        Start to run the thread method
        :param thread_count: the count of threads
        :param kwargs:
        :return:
        """
        for t in range(thread_count):
            threading = self.__Thread(self.__method, **kwargs)
            threading.start()
            self.__threads.append(threading)

    def wait(self) -> None:
        """
        Waiting for the running thread method to finish
        :return:
        """
        for t in self.__threads:
            t.join()
