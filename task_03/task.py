import os

from string import ascii_lowercase, ascii_uppercase


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''

PRIORITIES = {
    **{c: i + 1 for i, c in enumerate(ascii_lowercase)},
    **{c: i + 27 for i, c in enumerate(ascii_uppercase)},
}


def line_priority(line: str) -> int:
    middle = len(line) // 2
    lhs, rhs = line[:middle], line[middle:]

    common_item = list(set(lhs) & set(rhs))[0]
    return PRIORITIES[common_item]


def group_priority(group: list[str]) -> int:
    g_a, g_b, g_c = group

    common_item = set(g_a) & set(g_b) & set(g_c)
    assert len(common_item) == 1
    badge = list(common_item)[0]
    return PRIORITIES[badge]


def iter_groups(data: str):
    lines = data.splitlines()
    n_strides = len(lines) // 3
    yield from [lines[i * 3:(i + 1) * 3] for i in range(n_strides)]


def priority_sum(data: str):
    total_priorities = [line_priority(line) for line in data.splitlines()]
    yield sum(total_priorities)

    group_priorities = [group_priority(g) for g in iter_groups(data)]
    yield sum(group_priorities)


if __name__ == '__main__':
    test_case = priority_sum(TEST_DATA)
    assert next(test_case) == 157
    assert next(test_case) == 70

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = priority_sum(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
