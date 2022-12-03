import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
A Y
B X
C Z
'''

SCORES = {
    'rock': 1,
    'paper': 2,
    'scissors': 3,
}
MOVES = {
    'A': 'rock',
    'X': 'rock',
    'B': 'paper',
    'Y': 'paper',
    'C': 'scissors',
    'Z': 'scissors',
}

OUTCOMES = {
    'X': 'lose',
    'Y': 'draw',
    'Z': 'win',
}
WIN_LOSE_MOVES = {
    'rock': ['paper', 'scissors'],
    'paper': ['scissors', 'rock'],
    'scissors': ['rock', 'paper'],
}


def score_1(line):
    r_i, r_j = line.split()
    m_a, m_b = MOVES[r_i], MOVES[r_j]
    score = SCORES[m_b]

    did_win = any([
        m_a == 'scissors' and m_b == 'rock',    # rock defeats scissors
        m_a == 'paper' and m_b == 'scissors',   # scissors defeats paper
        m_a == 'rock' and m_b == 'paper',       # paper defeats rock
    ])

    if did_win:
        score += 6
    elif m_a == m_b:
        score += 3  # was a draw

    return score

def score_2(line):
    i, j = line.split()
    move, outcome = MOVES[i], OUTCOMES[j]

    score = 0

    if outcome == 'win':
        my_move = WIN_LOSE_MOVES[move][0]
        score = 6 + SCORES[my_move]
    if outcome == 'lose':
        my_move = WIN_LOSE_MOVES[move][1]
        score = SCORES[my_move]
    if outcome == 'draw':
        my_move = move
        score = 3 + SCORES[my_move]

    return score


def total_score(data):
    scores_1 = [score_1(line) for line in data.splitlines()]
    yield sum(scores_1)

    scores_2 = [score_2(line) for line in data.splitlines()]
    yield sum(scores_2)


if __name__ == '__main__':
    test_case = total_score(TEST_DATA)
    assert next(test_case) == 15
    assert next(test_case) == 12

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = total_score(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
