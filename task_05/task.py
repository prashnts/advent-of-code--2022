import os
import re

from collections import namedtuple
from typing import List, Dict, Tuple


__here__ = os.path.dirname(__file__)

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    # To preserve trailing spaces, test data isn't inlined.
    TEST_DATA = fp.read()

RearrangementRule = namedtuple('RearrangementRule', ['count', 'src', 'dest'])
StackT = Dict[int, List[str]]


def parse_rearrangement(line: str) -> RearrangementRule:
    rule_fmt = r'move (\d+) from (\d+) to (\d+)'
    a, b, c = map(int, re.match(rule_fmt, line).groups())
    return RearrangementRule(count=a, src=b, dest=c)

def parse_stack(stacks: List[str]) -> StackT:
    last_row = stacks.pop(-1)
    n_line = len(last_row)
    n_rows = (n_line // 4) + 1   # stride length is 4

    stack = {i + 1: [] for i in range(n_rows)}

    for line in stacks:
        # take every element at strides, starting from index 1.
        items = [line[i] for i in range(1, n_line, 4)]
        # fill the relevant stacks; top of stack is the last element.
        for i, item in enumerate(items):
            if item != ' ':
                stack[i + 1].insert(0, item)
    return stack

def parse_input(data: str) -> Tuple[StackT, List[RearrangementRule]]:
    stacks = []
    rearrangements = []

    reading_stack = True

    for line in data.splitlines():
        if line == '':
            # split to rules at empty line
            reading_stack = False
            continue

        if reading_stack:
            stacks.append(line)
        else:
            rearrangements.append(parse_rearrangement(line))

    return parse_stack(stacks), rearrangements

def apply_rearrangement(stack: StackT, rules: List[RearrangementRule], one_by_one=True) -> StackT:
    # Note: modifies stack in place!
    for rule in rules:
        # move [count] from [src] to [dest]
        if one_by_one:
            for _ in range(rule.count):
                stack[rule.dest].append(stack[rule.src].pop())
        else:
            src = stack[rule.src]
            stack[rule.src] = src[:-rule.count]
            stack[rule.dest] += src[-rule.count:]
    return stack

def top_of_the_stack(stack: StackT) -> str:
    return ''.join([stack[r + 1][-1] for r in range(len(stack))])

def stack_state(data: str):
    stack_1 = apply_rearrangement(*parse_input(data))

    yield top_of_the_stack(stack_1)

    stack_2 = apply_rearrangement(*parse_input(data), one_by_one=False)
    yield top_of_the_stack(stack_2)


if __name__ == '__main__':
    test_case = stack_state(TEST_DATA)
    assert next(test_case) == 'CMZ'
    assert next(test_case) == 'MCD'

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = stack_state(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
