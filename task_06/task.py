import os

from typing import Iterator, Tuple

__here__ = os.path.dirname(__file__)

TEST_DATA = [
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, 19),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5, 23),
    ('nppdvjthqldpwncqszvftbrmjlhg', 6, 23),
    ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, 29),
    ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, 26),
]

def iter_chunks(data: str, n_chunk: int = 4) -> Iterator[Tuple[int, str]]:
    n_items = len(data)
    for i in range(n_items - (n_chunk - 1)):
        yield i, data[i:i + n_chunk]

def first_marker_pos(packet: str, chunklen: int) -> int:
    for pos, chunk in iter_chunks(packet, n_chunk=chunklen):
        if len(chunk) == len(set(chunk)):
            return pos + chunklen

def packet_start(data: str):
    yield first_marker_pos(data, chunklen=4)
    yield first_marker_pos(data, chunklen=14)


if __name__ == '__main__':
    for test_line, start_of_packet, start_of_message in TEST_DATA:
        test_case = packet_start(test_line)
        assert next(test_case) == start_of_packet
        assert next(test_case) == start_of_message

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = packet_start(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
