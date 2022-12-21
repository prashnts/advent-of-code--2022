import os
import json

from collections import namedtuple
from itertools import zip_longest
from typing import Iterator

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''

PacketPair = namedtuple('PacketPair', ['index', 'a', 'b'])

def parse_input(data: str) -> Iterator[PacketPair]:
    groups = data.strip().split('\n\n')

    for ix, pair in enumerate(groups):
        pa, pb = pair.split('\n')
        yield PacketPair(ix + 1, json.loads(pa), json.loads(pb))


def compare_packet(a, b):
    if type(a) == type(b) == int:
        # both are integers.
        if a < b:
            # left is smaller, so right order.
            return True
        if a == b:
            # equal, so continue.
            return None
        return False
    elif type(a) == type(b) == list:
        # both are lists, iterate their elements.
        for a1, b1 in zip_longest(a, b, fillvalue=None):
            if a1 is None:
                # left list ran out, input in right order.
                return True
            if b1 is None:
                # right list ran out, input is not in right order.
                return False

            comparison = compare_packet(a1, b1)

            if comparison is None:
                # No conclusion, so continue looping.
                continue

            return comparison
    else:
        # they dont match type
        if type(a) == int:
            return compare_packet([a], b)
        else:
            return compare_packet(a, [b])

def sort_packets(packets):
    # Basic bubble sort.
    packets = packets[:]
    for i in range(len(packets)):
        for j in range(0, len(packets) - i - 1):
            if compare_packet(packets[j], packets[j + 1]) == False:
                packets[j], packets[j + 1] = packets[j + 1], packets[j]
    return packets


def packet_parity(data: str):
    pairs = list(parse_input(data))

    ordered_pairs = []

    for pair in pairs:
        if compare_packet(pair.a, pair.b):
            ordered_pairs.append(pair.index)

    yield sum(ordered_pairs)

    divider_a = [[2]]
    divider_b = [[6]]

    packets = [divider_a, divider_b]

    for pair in pairs:
        packets.append(pair.a)
        packets.append(pair.b)

    # now we sort.
    packets = sort_packets(packets)

    decoder_key_a = packets.index(divider_a) + 1
    decoder_key_b = packets.index(divider_b) + 1
    yield decoder_key_a * decoder_key_b


if __name__ == '__main__':
    test_case = packet_parity(TEST_DATA)
    assert next(test_case) == 13
    assert next(test_case) == 140

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = packet_parity(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
