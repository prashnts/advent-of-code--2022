import os
import heapq as heap

from collections import defaultdict

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

def gen_neighbors(array, x, y):
    '''Generated value and coordinates in NSWE directions.'''
    dirs = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]
    sx = len(array)
    sy = len(array[0])
    my_value = array[x][y]

    for x, y in dirs:
        if not(0 <= x < sx and 0 <= y < sy):
            # bounds check
            continue
        neighbor = array[x][y]
        if neighbor <= my_value + 1:
            yield neighbor, (x, y)


def reconstruct_paths(predecessors, source, target):
    # Invert the predecessors dict.
    successors = defaultdict(list)

    for parent, child in predecessors.items():
        successors[child].append(parent)

    paths = []

    def traverse(node, initial_path):
        # dfs to find all the paths.
        path = initial_path[:]
        path.append(node)

        for successor in successors[node]:
            if successor == target:
                paths.append(path)
            else:
                traverse(successor, path)

    traverse(source, [])

    return paths


def dijkstra(weights, start_node, end_node):
    # Taken from my solution to task 15 of 2021's challenge.
    # Kind of modified to ignore "cost", since we are interested in stride costs
    # only.
    visited = set()
    parents_map = {}
    pq = []
    node_costs = defaultdict(lambda: float('inf'))
    node_costs[start_node] = 0
    heap.heappush(pq, (0, start_node))

    while pq:
        # go greedily by always extending the shorter cost nodes first
        _, node = heap.heappop(pq)
        if node == end_node:
            break
        visited.add(node)

        for _, adj_node in gen_neighbors(weights, node[0], node[1]):
            if adj_node in visited:
                continue

            new_cost = node_costs[node] + 1     # the path weight is increased by one,
                                                # not by the node's weight.
            if node_costs[adj_node] > new_cost:
                parents_map[adj_node] = node
                node_costs[adj_node] = new_cost
                heap.heappush(pq, (new_cost, adj_node))

    return parents_map, node_costs


def parse_input(data: str):
    space = [list(line) for line in data.splitlines()]
    x_span = len(space)
    y_span = len(space[0])

    # We transform the elevation map into a grid-graph.
    graph = []
    start = None
    dest = None

    for x in range(x_span):
        row = []
        for y in range(y_span):
            elevation = space[x][y]
            if elevation == 'S':
                start = (x, y)
                elevation = 'a'
            elif elevation == 'E':
                dest = (x, y)
                elevation = 'z'

            row.append(ord(elevation) - ord('a'))
        graph.append(row)

    return graph, start, dest


def shitty_signals(data: str):
    graph, start, dest = parse_input(data)

    predecessors, _ = dijkstra(graph, start, dest)
    paths = reconstruct_paths(predecessors, start, dest)

    yield min(map(len, paths))

    # for part 2, find all the points where weight == 0.
    start_points = []

    for x, row in enumerate(graph):
        for y, cell in enumerate(row):
            if cell == 0:
                start_points.append((x, y))

    shortest_path_lens = []

    print(f'Enumerating {len(start_points)} start points. This may take a little while.')

    for start in start_points:
        predecessors, _ = dijkstra(graph, start, dest)
        paths = reconstruct_paths(predecessors, start, dest)

        if paths:
            shortest_path_lens.append(min(map(len, paths)))

    yield min(shortest_path_lens)


if __name__ == '__main__':
    test_case = shitty_signals(TEST_DATA)
    assert next(test_case) == 31
    assert next(test_case) == 29

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = shitty_signals(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
