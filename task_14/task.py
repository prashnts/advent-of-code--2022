# Not the proudest solution! It's quite slow for the second part, but it's a
# verbatim implementation -- can't be simpler IMO.
import os

from enum import Enum
from collections import namedtuple
from typing import Dict

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''


Point = namedtuple('Point', ['x', 'y'])
BoardSpan = namedtuple('BoardShape', ['x_min', 'x_max', 'y_min', 'y_max'])

class Shape(Enum):
    # Of course not all the combinations are valid.
    rock = '#'   # am I a rock?
    air = '.'    # or just some air?
    sand = 'o'   # just a flick of sand...
    source = '+'

class Board:
    def __init__(self, source: Point):
        self.space: Dict[Point, Shape] = {}
        self.space[source] = Shape.source
        self.source = source
        self.floor = None

    def __getitem__(self, key: Point) -> Shape:
        try:
            if self.floor is not None and key.y == self.floor:
                return Shape.rock
            return self.space[key]
        except KeyError:
            return Shape.air

    def __setitem__(self, key: Point, value: Shape):
        self.space[key] = value

    @property
    def span(self) -> BoardSpan:
        # what's the horizontal and vertical range?
        pts = [*self.space.keys(), self.source]
        x = [pt.x for pt in pts]
        y = [pt.y for pt in pts]
        return BoardSpan(min(x), max(x), min(y), max(y))

    @property
    def deepest_rock(self) -> int:
        rock_levels = [pt.y for pt, shape in self.space.items() if shape == Shape.rock]
        return max(rock_levels)

    def show(self) -> str:
        span = self.span
        canvas = [[
            Shape.air.value
            for _ in range(span.x_min, span.x_max + 1)]
            for _ in range(span.y_min, span.y_max + 1)
        ]
        for pt, shape in self.space.items():
            canvas[pt.y - span.y_min][pt.x - span.x_min] = shape.value

        return '\n'.join([''.join(row) for row in canvas])

    def set_floor(self, level):
        self.floor = level

    @property
    def sand_count(self):
        return len([pt for pt, shape in self.space.items() if shape == Shape.sand])


def iter_path(a: Point, b: Point):
    if a.x == b.x:
        # vertical line
        for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
            yield Point(a.x, y)
    elif a.y == b.y:
        # horizontal line
        for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
            yield Point(x, a.y)
    else:
        raise NotImplementedError("Only horizontal or vertical lines please.")


def parse_input(data: str) -> Board:
    board = Board(source=Point(500, 0))

    def parse_line(line):
        points = [Point(*map(int, coord.split(','))) for coord in line.split(' -> ')]

        for a, b in zip(points, points[1:]):
            for pt in iter_path(a, b):
                board[pt] = Shape.rock

    for line in data.splitlines():
        parse_line(line)

    return board


def drop_sand(board, bound_check=True):
    def move_sand(pt):
        neighbors = [
            Point(pt.x, pt.y + 1),      # down
            Point(pt.x - 1, pt.y + 1),  # left diagonal
            Point(pt.x + 1, pt.y + 1),  # right diagonal
        ]
        for ps in neighbors:
            if board[ps] == Shape.air:
                board[pt] = Shape.air   # clear old location
                board[ps] = Shape.sand
                return ps
        return pt

    # Drop a sand from source...
    pos = board.source
    span = board.span
    did_move = 1

    while True:
        new_pos = move_sand(pos)

        if new_pos == pos:
            # stop moving
            break
        did_move += 1
        # bounds check
        if bound_check is True and not all([
            span.x_min <= new_pos.x <= span.x_max,
            span.y_min <= new_pos.y <= span.y_max,
        ]):
            # it goes to infinite, stop simulation. and remove it from board
            board[new_pos] = Shape.air
            raise StopIteration('Out of bounds')

        pos = new_pos

    return board, did_move


def sandulator(data: str):
    board = parse_input(data)

    try:
        while True:
            board, _ = drop_sand(board, bound_check=True)
    except StopIteration:
        pass

    yield board.sand_count

    # we continue the simulation...
    board.set_floor(board.deepest_rock + 2)

    # and continue the simulation!
    print('this will take a while...')
    while True:
        try:
            board, did_move = drop_sand(board, bound_check=False)
            if did_move == 1:
                break
        except StopIteration:
            pass

    yield board.sand_count + 1  # add one for good luck!
                                # (the source is empty so we compensate)


if __name__ == '__main__':
    test_case = sandulator(TEST_DATA)
    assert next(test_case) == 24
    assert next(test_case) == 93

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = sandulator(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
