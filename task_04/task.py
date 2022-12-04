import os


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''


def bounds(line):
    p_a, p_b = line.split(',')
    a_x, a_y = map(int, p_a.split('-'))
    b_x, b_y = map(int, p_b.split('-'))
    return a_x, a_y, b_x, b_y


def fully_overlaps(line):
    a_x, a_y, b_x, b_y = bounds(line)
    return any([
        a_x <= b_x and a_y >= b_y,
        b_x <= a_x and b_y >= a_y,
    ])


def any_overlap(line):
    '''
    Overlap strategy:

      a_x   |===========|   a_y
      b_x       |****|      b_y     } a_x <= b_x & a_y >= b_x
      b_x       |*******--| b_y     }./
      b_x |--*****|         b_y     } a_x >= b_x & a_x <= b_y
      b_x |--***********--| b_y     }./
    '''
    a_x, a_y, b_x, b_y = bounds(line)
    return any([
        a_x <= b_x and a_y >= b_x,
        a_x >= b_x and a_x <= b_y,
    ])


def common_pairs(data: str):
    pairs = [True for line in data.splitlines() if fully_overlaps(line)]
    yield len(pairs)

    pairs = [True for line in data.splitlines() if any_overlap(line)]
    yield len(pairs)


if __name__ == '__main__':
    test_case = common_pairs(TEST_DATA)
    assert next(test_case) == 2
    assert next(test_case) == 4

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = common_pairs(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
