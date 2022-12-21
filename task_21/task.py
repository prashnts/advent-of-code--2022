# As an exception, this solution uses `sympy` to solve a linear equation for part 2.
import os
import operator

from collections import namedtuple

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

Expression = namedtuple('Expression', ['lhs', 'op', 'rhs'])

def parse_input(data: str) -> tuple[dict, dict]:
    scalars = {}
    expressions = {}
    for line in data.splitlines():
        m_name, eqn = line.split(': ')
        try:
            scalar = int(eqn)
            scalars[m_name] = scalar
        except ValueError:
            # its an expression.
            lhs, op, rhs = eqn.split(' ')
            expressions[m_name] = Expression(lhs, OPS[op], rhs)

    return scalars, expressions


def broken_calculator(data: str) -> int:
    # Part 1
    scalars, expressions = parse_input(data)

    while 'root' not in scalars:
        # keep simplifying the expressions.
        for monkey, exp in expressions.copy().items():
            try:
                scalars[monkey] = exp.op(scalars[exp.lhs], scalars[exp.rhs])
                del expressions[monkey]
            except KeyError:
                continue

    return int(scalars['root'])


def working_calculator(data: str) -> int:
    # Part 2: find what causes the equation root to be true. The two while
    # loops may be merged.
    try:
        from sympy import Symbol
        from sympy.solvers import solve
    except ImportError:
        print('[!] Part 2 requires sympy.')
        return 301 # default input
    scalars, expressions = parse_input(data)
    # know that monkey, you, `humn` is no longer speaking.
    del scalars['humn']
    root = expressions['root']

    # we will simplify the lhs and rhs of `root` eqn separately.
    while not (root.lhs in scalars or root.rhs in scalars):
        # similarly, simplify as much as we can.
        for monkey, exp in expressions.copy().items():
            try:
                scalars[monkey] = exp.op(scalars[exp.lhs], scalars[exp.rhs])
                del expressions[monkey]
            except KeyError:
                continue

    # get the solved part of root equation.
    other_monkey: str
    target: int
    if root.lhs in scalars:
        target = scalars[root.lhs]
        other_monkey = root.rhs
    else:
        target = scalars[root.rhs]
        other_monkey = root.lhs

    # create a sympy expression
    humn = Symbol('humn')
    scalars['humn'] = humn

    while other_monkey not in scalars:
        # continue solving, but now `humn` will stay as a symbol.
        for monkey, exp in expressions.copy().items():
            try:
                scalars[monkey] = exp.op(scalars[exp.lhs], scalars[exp.rhs])
                del expressions[monkey]
            except KeyError:
                continue

    # The other_monkey should have final value == target.
    # Sympy expression assumes we're solving for zero.
    eqn = target - scalars[other_monkey]
    soln = solve(eqn, humn)[0]
    return int(soln)


def monkey_calculator(data: str):
    yield broken_calculator(data)
    yield working_calculator(data)


if __name__ == '__main__':
    test_case = monkey_calculator(TEST_DATA)
    assert next(test_case) == 152
    assert next(test_case) == 301

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = monkey_calculator(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
