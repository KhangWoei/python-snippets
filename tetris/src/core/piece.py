from abc import ABC, abstractmethod
from typing import List
from random import choice

class Piece(ABC):
    def __init__(self, y: int = 0, x: int =0) -> None:
        self._x = x
        self._y = y
        self._shape: List[List[int]] = []

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def shape(self) -> List[List[int]]:
        return self._shape

class IPiece(Piece):
    def __init__(self, y: int = 0, x: int =0) -> None:
        super().__init__(y, x)
        self._shape = [[1, 1, 1, 1]]

class TPiece(Piece):
    def __init__(self, y: int = 0, x: int =0) -> None:
        super().__init__(y, x)
        self._shape = [
            [0, 1, 0],
            [1, 1, 1]
        ]

class RandomPieceFactory:
    _PIECES = [IPiece, TPiece]

    @staticmethod
    def create(y: int = 0, x: int = 0) -> Piece:
        return choice(RandomPieceFactory._PIECES)(y, x)
