from typing import List, Tuple, Any
import random
from common import Step, Direction, EntityType, opositeDirection
from Board import Board
from DrawingStrategy import DrawingStrategy


def addTuples(tuple1: Tuple, tuple2: Tuple) -> Tuple:
    return tuple(value1 + value2 for value1, value2 in zip(tuple1, tuple2))


class DirectionManager:
    currentDirection: Direction

    def __init__(self, direction):
        self.newDirection = None
        self.currentDirection = direction

    def changeDirection(self, direction):
        if not self.newDirection:
            if direction is not opositeDirection[self.currentDirection]:
                self.newDirection = direction

    def popDirection(self):
        if self.newDirection:
            self.currentDirection = self.newDirection
            self.newDirection = None

        return self.currentDirection


class Entity:
    positions: List[Tuple[int, int]]
    board: Board
    type: EntityType

    def CollidesWith(self, other: 'Entity') -> bool:
        for position in self.positions:
            if position in other.positions:
                return True

        return False


class Snake(Entity):
    entityType: EntityType = EntityType.SNAKE
    headStyle: DrawingStrategy
    bodyStyle: DrawingStrategy

    def __init__(self, board: Board):
        self.board = board
        self.positions = [(3, 1), (2, 1), (1, 1)]

        self.board.occupyCells(self.positions, Snake.entityType)

    @property
    def headPosition(self) -> Tuple[int, int]:
        return self.positions[0]

    @property
    def tailPosition(self) -> Tuple[int, int]:
        return self.positions[-1]

    def move(self, direction: Direction) -> None:
        self.expand(direction)
        self.board.abandonCell(self.tailPosition)
        self.positions.pop()

    def expand(self, headDirection: Direction) -> None:
        newHeadPosition = addTuples(self.headPosition, Step[headDirection])

        self.positions.insert(0, newHeadPosition)
        self.board.occupyCell(newHeadPosition, Snake.entityType)

    def intersectsItself(self) -> bool:
        return self.headPosition in self.positions[1:]

    def draw(self):
        self.headStyle.draw(self.headPosition)

        for point in self.positions[1:]:
            self.bodyStyle.draw(point)


class Food(Entity):
    entityType: EntityType = EntityType.FOOD
    style: DrawingStrategy

    def __init__(self, board: Board):
        self.board = board
        self.randomizePosition()
        self.board.occupyCell(self.positions[0], Food.entityType)

    def eaten(self) -> None:
        self.board.abandonCell(self.positions[0])
        self.randomizePosition()
        self.board.occupyCell(self.positions[0], Food.entityType)

    def randomizePosition(self) -> None:
        self.positions = [random.choice(self.board.getEmptyCells())]

    def draw(self):
        self.style.draw(self.positions[0])
