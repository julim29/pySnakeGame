from enum import Enum
import pygame


class EntityType(Enum):
    SNAKE = 0
    FOOD = 1
    WALL = 2


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


keyMap = {
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_UP: Direction.UP,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT
}

opositeDirection = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT
}

Step = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0)
}
