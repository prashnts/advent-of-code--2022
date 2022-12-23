# Only Part 1.
import os
import re
import time

from collections import namedtuple
from typing import NamedTuple

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''

OPEN = '.'
CLOSED = '#'

class Pt(NamedTuple):
    r: int  # row
    c: int  # col

    def __add__(self, other: 'Pt') -> 'Pt':
        a = self
        b = other
        return Pt(a.r + b.r, a.c + b.c)


class Pos(NamedTuple):
    r: int
    c: int

    f: int  # "facing"    3>0
            #           2<1

    @property
    def point(self) -> Pt:
        return Pt(self.r, self.c)


STEPS = {
    0: Pt(0, 1),      # Right
    1: Pt(1, 0),      # Down
    2: Pt(0, -1),     # Left
    3: Pt(-1, 0),     # Up
}
DARROWS = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^',
}


def parse_input(data: str) -> tuple[dict, list]:
    mmap, path = data.split('\n\n')
    mhash = {}

    for r, row in enumerate(mmap.splitlines()):
        for c, cell in enumerate(row):
            if cell == ' ':
                continue
            # add cell to map.
            mhash[Pt(r, c)] = cell

    path = re.split(r'([RL])', path)
    path[::2] = map(int, path[::2])

    return mhash, path


class MonkeyMap:
    def __init__(self, mhash: dict[Pt, str]):
        self.mmap = self.preload(mhash)
        self.path = []

    def preload(self, mhash):
        pts = mhash.keys()
        origin = min(pts)
        assert mhash[origin] == OPEN
        self.pos = Pos(*origin, 0)   # begin facing right, so f=0

        # set the bounds.
        rows, cols = zip(*pts)
        self.row_min = min(rows)
        self.row_max = max(rows)
        self.col_min = min(cols)
        self.col_max = max(cols)

        return mhash

    def move(self, step):
        if type(step) == str:
            turn = 1 if step == 'R' else -1
            p = self.pos
            # change angle
            facing = (p.f + turn) % 4
            self.pos = Pos(p.r, p.c, facing)
        else:
            for _ in range(step):
                new_pos = self.make_step()
                self.path.append(new_pos)
                self.pos = new_pos
        return self.pos

    def make_step(self):
        # Step always moves us forward in our own heading.
        # find next
        p = self.pos

        step = STEPS[p.f]

        next_pos = p.point + step

        if next_pos not in self.mmap:
            # next point is then a void. we need to find the wrap-around point.
            # thankfully the map does not contain holes, so we are safer.
            # find the opposite point in the direction.
            # get current row and col coords.
            row = [pt for pt in self.mmap.keys() if pt.c == p.c]
            col = [pt for pt in self.mmap.keys() if pt.r == p.r]

            if p.f == 0:
                next_pos = min(col)
            if p.f == 1:
                next_pos = min(row)
            if p.f == 2:
                next_pos = max(col)
            if p.f == 3:
                next_pos = max(row)

        if self.mmap[next_pos] == OPEN:
            # we can step here! so we do it
            return Pos(*next_pos, p.f)
        else:
            # we cannot step on CLOSED point.
            return p

    def show(self):
        screen = [
            [' ' for _ in range(self.col_min, self.col_max + 1)]
            for _ in range(self.row_min, self.row_max + 1)]

        for pt, cell in self.mmap.items():
            screen[pt.r][pt.c] = cell

        for pt in self.path:
            screen[pt.r][pt.c] = f'\033[32m{DARROWS[pt.f]}\033[0m'

        return '\n'.join([''.join(row) for row in screen])

class Cube:
    def __init__(self, mhash):
        # origin of the cubes.
        faces = {
            'a': Pt(0, 50),
            'b': Pt(0, 100),
            'c': Pt(50, 50),
            'd': Pt(50, 100),
            'e': Pt(0, 100),
            'f': Pt(0, 150),
        }

    def get_face(self, pt):
        pass

    def warp(self, pos: Pos):
        # derive next position from pos in the direction we face.
        pass


def monkeypass(data: str, debug=False):
    mhash, path = parse_input(data)

    mmap = MonkeyMap(mhash)

    for step in path:
        mmap.move(step)
        if debug:
            print('\033[2J')
            print(step)
            print(mmap.show())
            # time.sleep(0.5)

    yield 1000 * (mmap.pos.r + 1) + 4 * (mmap.pos.c + 1) + mmap.pos.f


if __name__ == '__main__':
    test_case = monkeypass(TEST_DATA, debug=True)
    assert next(test_case) == 6032
    # assert next(test_case) == 301

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = monkeypass(data)
    print(f'answer_1={next(answers)}')
    # print(f'answer_2={next(answers)}')
