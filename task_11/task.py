import re
import os
import operator

from typing import List, Iterator, Tuple


__here__ = os.path.dirname(__file__)

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    TEST_DATA = fp.read()


OPS = {
    '+': operator.add,
    '*': operator.mul,
}


class Monkey:
    def __init__(self, index, items, operation, destination, divisor):
        self.index = index
        self.items = items
        self.operation = operation
        self.destination = destination
        self.divisor = divisor
        self.inspection_count = 0

    def inspect_and_throw(self, relief: int = None) -> Tuple[int, int]:
        item = self.items.pop(0)    # take the first item
        new_item = self.operation(item)
        if relief is None:
            new_item = new_item // 3
        else:
            new_item = new_item % relief
        self.inspection_count += 1
        return new_item, self.destination(new_item)

    def catch(self, item):
        self.items.append(item)

    def __repr__(self):
        return f'Monkey {self.index}: {self.items}'


def parse_input(data: str) -> Iterator[Monkey]:
    monkeys = data.split('\n\n')

    def parse_monkey(monkey) -> Monkey:
        m = monkey.split('\n')
        index = int(re.match(r'Monkey (\d+):', m[0]).groups()[0])
        items = list(map(int, m[1].split(': ')[1].split(', ')))
        lhs, op, rhs = re.match(r'.+ new = (.+) ([\+\*]) (.+)$', m[2]).groups()
        divisor = int(m[3].split('by ')[1])
        dest_true = int(m[4].split('monkey ')[1])
        dest_false = int(m[5].split('monkey ')[1])

        operation = lambda x: OPS[op](
            x if lhs == 'old' else int(lhs),
            x if rhs == 'old' else int(rhs)
        )
        destination = lambda x: dest_true if x % divisor == 0 else dest_false

        return Monkey(index, items, operation, destination, divisor)

    yield from map(parse_monkey, monkeys)


def simulate_monkey_biz(monkeys: List[Monkey], rounds: int) -> int:
    if rounds == 20:
        relief = None
    else:
        # Yay, large numbers!
        # When we're simulating without relief, the numbers grow very quickly.
        # for our purposes, we need to reduce them by a factor that still keeps
        # the division operations correct. This is achieved by multiplying all
        # the divisors together to obtain the period of worry levels. In this
        # period all the individual divisions are correct, and so are addition.
        relief = 1
        for m in monkeys:
            relief *= m.divisor

    def simulate_round():
        for monkey in monkeys:
            while True:
                try:
                    item, dest = monkey.inspect_and_throw(relief=relief)
                except IndexError:
                    break
                else:
                    monkeys[dest].catch(item)

    for _ in range(rounds):
        simulate_round()

    inspections = sorted([m.inspection_count for m in monkeys], reverse=True)
    return inspections[0] * inspections[1]


def monkey_biz(data: str):
    yield simulate_monkey_biz(list(parse_input(data)), rounds=20)
    yield simulate_monkey_biz(list(parse_input(data)), rounds=10000)


if __name__ == '__main__':
    test_case = monkey_biz(TEST_DATA)
    assert next(test_case) == 10605
    assert next(test_case) == 2713310158

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = monkey_biz(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
