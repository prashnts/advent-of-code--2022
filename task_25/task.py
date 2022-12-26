import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''

DIGITS = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

NUMERALS = {
    0: '0',
    1: '1',
    2: '2',
    3: '=',  # 5 - 2
    4: '-',  # 5 - 1
}


def snafu_to_int(num: str) -> int:
    val = 0

    for i, d in enumerate(num[::-1]):
        val += DIGITS[d] * (5 ** i)

    return val

def int_to_snafu(num: int) -> str:
    snafu = []
    q = num

    while q:
        r = q % 5       # remainder
        q = q // 5      # quotient
        if r == 3 or r == 4:
            # offset quotient by one to account for the remaining 5.
            q += 1
        snafu.append(NUMERALS[r])

    return ''.join(snafu[::-1])


def double_minus(data: str, debug=False):
    fuel_level = sum(map(snafu_to_int, data.splitlines()))
    yield int_to_snafu(fuel_level)


if __name__ == '__main__':
    test_case = double_minus(TEST_DATA, debug=True)
    assert next(test_case) == '2=-1=0'

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = double_minus(data)
    print(f'answer_1=\033[32m{next(answers)}\033[0m')
