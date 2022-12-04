import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''


def grouped_max(data):
    groups = []
    group = []

    for line in data.splitlines():
        if line == '':
            groups.append(sum(group))
            group = []
            continue
        group.append(int(line))
    # Last group
    groups.append(sum(group))

    # Top elf
    yield max(groups)

    # Top 3 elves
    groups.sort(reverse=True)
    yield sum(groups[:3])


if __name__ == '__main__':
    test_case = grouped_max(TEST_DATA)
    assert next(test_case) == 24000
    assert next(test_case) == 45000

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = grouped_max(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
