import json
from abc import ABCMeta, abstractmethod


class BaseModel(metaclass=ABCMeta):
    __abstract__ = True

    @abstractmethod
    def __init__(self, row: dict): pass

    @property
    def dict(self):
        return {
            attr: self.__getattribute__(attr)
            for attr in dir(self)
            if attr != 'dict' and attr[0] != '_'
        }

    def __repr__(self) -> str:
        return json.dumps(self.dict)
