import os

from typing import List, Iterator, Optional, Tuple


__here__ = os.path.dirname(__file__)

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    TEST_DATA = fp.read()


class Computer:
    r_x: int = 1    # the register x
    pc: int = 0     # program/cycle counter

    sig_cycle = [20, 60, 100, 140, 180, 220]
    signals: List[int]

    screen: List[int]

    def __init__(self):
        self.signals = []
        self.screen = []

    @property
    def signal_strength(self) -> int:
        return sum(self.signals)

    @property
    def sprite(self) -> List[int]:
        x = self.r_x
        return [x - 1, x, x + 1]

    def tick(self):
        # Ticks the computer. At each tick, CRT is drawn first then sig strength.
        self.draw()
        self.pc += 1
        if self.pc in self.sig_cycle:
            self.signals.append(self.pc * self.r_x)

    def draw(self):
        x = self.pc % 40
        if x in self.sprite:
            self.screen.append(1)
        else:
            self.screen.append(0)

    def exec(self, instr: str, arg: int = None):
        if instr == 'noop':
            self.tick()
        if instr == 'addx':
            self.tick()
            self.tick()
            self.r_x += arg

    def render_screen(self):
        n = 40
        mapper = lambda x: '\033[34m█' if x else '\033[90m≣'
        view = '\n'.join([
            ''.join(map(mapper, self.screen[i:i + n]))
            for i in range(0, len(self.screen), n)
        ])
        return view


def parse_input(data: str) -> Iterator[Tuple[str, Optional[int]]]:
    for line in data.splitlines():
        inst = line.split(' ')
        if len(inst) == 2:
            yield inst[0], int(inst[1])
        else:
            yield inst[0], None


def sys_emulator(data: str):
    computer = Computer()

    for instr, arg in parse_input(data):
        computer.exec(instr, arg)

    yield computer.signal_strength
    yield computer.render_screen()


if __name__ == '__main__':
    test_case = sys_emulator(TEST_DATA)
    assert next(test_case) == 13140
    # print(next(test_case))

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = sys_emulator(data)
    print(f'answer_1={next(answers)}')
    print('for answer 2, check output below:')
    print(next(answers))
