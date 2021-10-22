import numpy as np
from common import EntityType
from typing import List, Tuple, Any


class Board:
    cells: np.ndarray  # EntityType ndarray

    def __init__(self, boardsize: Tuple[int, int]):
        self.cells = np.empty(boardsize, dtype=EntityType)

    def getEmptyCells(self) -> List[Tuple[int, int]]:
        return list(zip(*np.where(self.cells == None)))

    def occupyCell(self, cell: Tuple[int, int], entitytype: EntityType) -> None:
        if cell[0] < 0 or cell[1] < 0:
            raise IndexError("There are no negative indices.")
        self.cells[cell] = entitytype

    def occupyCells(self, cells: List[Tuple[int, int]], entitytype: EntityType) -> None:
        for cell in cells:
            if cell[0] < 0 or cell[1] < 0:
                raise IndexError("There are no negative indices.")

            self.cells[cell] = entitytype

    def abandonCell(self, cell: Tuple[int, int]) -> None:
        self.cells[cell] = None

    def getCellContent(self, cell: Tuple[int, int]) -> EntityType:
        return self.cells[cell]

    def isCellInsideBoard(self, cell: Tuple[int, int]) -> bool:
        try:
            self.cells[cell]
        except IndexError:
            return False

        return True
