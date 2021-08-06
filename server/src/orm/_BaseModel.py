import json
from abc import ABCMeta, abstractmethod


class BaseModel(metaclass=ABCMeta):
    __abstract__ = True

    @abstractmethod
    def __init__(self, row: dict): pass

    @property
    def dict(self):
        def _to_small_hump(name: str) -> str:
            words = name.split('_')
            result = [
                word[0].upper() + word[1:]
                for word in words
            ]
            result[0] = words[0]
            return ''.join(result)

        return {
            _to_small_hump(attr): self.__getattribute__(attr)
            for attr in dir(self)
            if attr != 'dict' and attr[0] != '_'
        }

    def __repr__(self) -> str:
        return json.dumps(self.dict)
