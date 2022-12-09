import os

from typing import Iterator, List, Tuple

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
TEST_DATA_2 = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def diagonals(self) -> List['Point']:
        x = self.x
        y = self.y

        return [
            Point(x - 1, y - 1),
            Point(x + 1, y - 1),
            Point(x - 1, y + 1),
            Point(x + 1, y + 1),
        ]

    @property
    def axials(self) -> List['Point']:
        x = self.x
        y = self.y

        return [
            Point(x - 1, y),
            Point(x + 1, y),
            Point(x, y - 1),
            Point(x, y + 1),
        ]

    @property
    def neighbors(self) -> Iterator['Point']:
        yield from self.axials
        yield from self.diagonals

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point<{self.x}, {self.y}>"

    def touches(self, other: 'Point') -> bool:
        # The points touch on axis, diagonally, or overlap.
        overlap = self == other
        in_neighborhood = any([x == other for x in self.neighbors])
        return overlap or in_neighborhood


MOVEMENTS = {
    'U': Point(0, 1),
    'D': Point(0, -1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
}


def move_tail(head: Point, tail: Point) -> Point:
    if not head.touches(tail):
        # update tail position.
        if tail.x == head.x:
            # tail is along x, so it must be moved in y direction towards head.
            dy = -1 if head.y < tail.y else 1
            tail = tail + Point(0, dy)
        elif tail.y == head.y:
            dx = -1 if head.x < tail.x else 1
            tail = tail + Point(dx, 0)
        else:
            # Check which diagonal position of tail makes it so that head
            # and tail touch.
            for loc in tail.diagonals:
                if head.touches(loc):
                    tail = loc
                    break
            else:
                # boundary check
                assert False
    return tail

def move_rope_segment(head: Point, tail: Point, dirn: str) -> Tuple[Point, Point]:
    delta = MOVEMENTS[dirn]

    head = head + delta
    tail = move_tail(head, tail)

    return head, tail

def move_rope(knots: List[Point], dirn: str) -> List[Point]:
    # head is the first knot, tail is the last one.
    delta = MOVEMENTS[dirn]
    head = knots[0]
    head = head + delta
    new_knots = [head]

    for tail in knots[1:]:
        tail = move_tail(head, tail)
        head = tail
        new_knots.append(tail)

    return new_knots

def parse_input(data: str) -> Iterator[Tuple[str, int]]:
    for line in data.splitlines():
        dirn, amount = line.split(' ')
        yield dirn, int(amount)

def plot_knots(tail_pos: List[Point]):
    # helper function to plot tail positions. change x/y ranges for bigger tails.
    x_range = 80
    y_range = 80

    surface = [['\033[34m░' for _ in range(x_range)] for _ in range(y_range)]
    x_mid = x_range // 2
    y_mid = x_range // 2

    for k in tail_pos:
        surface[y_mid - k.y][k.x - x_mid] = '\033[33m*'

    print('\n'.join([''.join(row) for row in surface]))
    print('\033[0m')

def simulate_small_rope(data):
    head = Point(0, 0)
    tail = Point(0, 0)

    tail_positions = []

    for dirn, amount in parse_input(data):
        for _ in range(amount):
            head, tail = move_rope_segment(head, tail, dirn)
            tail_positions.append(tail)

    return len(set(tail_positions))

def simulate_large_rope(data):
    knots = [Point(0, 0) for _ in range(10)]

    tail_positions = []

    for dirn, amount in parse_input(data):
        for _ in range(amount):
            knots = move_rope(knots, dirn)
            tail_positions.append(knots[-1])

    # plot_knots(tail_positions)
    return len(set(tail_positions))


def rope_motion(data: str):
    yield simulate_small_rope(data)
    yield simulate_large_rope(data)


if __name__ == '__main__':
    test_case = rope_motion(TEST_DATA)
    assert next(test_case) == 13
    assert next(test_case) == 1
    assert simulate_large_rope(TEST_DATA_2) == 36

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = rope_motion(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
