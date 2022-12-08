import os

from typing import Iterator, List

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
30373
25512
65332
33549
35390
'''

TreeMapT = List[List[int]]


def parse_input(data: str) -> TreeMapT:
    return [list(map(int, line)) for line in data.splitlines()]


def iter_tree_dirs(treemap: TreeMapT) -> Iterator:
    x_bound, y_bound = len(treemap), len(treemap[0])
    # create a column oriented view from row oriented treemap
    treemap_col = list(zip(*treemap))

    for x in range(x_bound):
        for y in range(y_bound):
            height = treemap[x][y]
            row = treemap[x]
            col = treemap_col[y]

            all_dirs = [
                row[:y][::-1],      # Left (inverted)
                row[(y + 1):],      # Right
                col[:x][::-1],      # Up (inverted)
                col[(x + 1):],      # Down
            ]

            yield x, y, height, all_dirs


def visible_trees(treemap: TreeMapT) -> int:
    visible = 0

    for _, _, height, directions in iter_tree_dirs(treemap):
        # tree is visible if all the trees in each dir are shorter.
        smaller_than_others = [height <= max(d) if d else False for d in directions]
        if not all(smaller_than_others):
            visible += 1

    return visible


def scenic_score(treemap: TreeMapT) -> int:
    scores = []

    for _, _, height, directions in iter_tree_dirs(treemap):
        viewing_dist = 1
        for d in directions:
            view = 0
            for tree in d:
                view += 1
                if tree >= height:
                    break
            viewing_dist *= view
        scores.append(viewing_dist)

    return max(scores)


def trees_count(data: str):
    yield visible_trees(parse_input(data))
    yield scenic_score(parse_input(data))


if __name__ == '__main__':
    test_case = trees_count(TEST_DATA)
    assert next(test_case) == 21
    assert next(test_case) == 8

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = trees_count(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
