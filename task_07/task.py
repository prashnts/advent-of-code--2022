import os

from collections import namedtuple
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import List, Union


__here__ = os.path.dirname(__file__)

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    TEST_DATA = fp.read()

TOTAL_DISK_SIZE   = 70000000
NEEDED_DISK_SPACE = 30000000

DirStat = namedtuple('DirStat', ['path', 'size'])


@dataclass
class File:
    path: PurePosixPath
    name: str
    size: int
    parent: 'Directory'


@dataclass
class Directory:
    '''Represents a "unix-like" filesystem with mutable content.'''
    path: PurePosixPath
    name: str
    content: List[Union[File, 'Directory']]
    parent: 'Directory' = None

    @property
    def size(self) -> int:
        return sum([item.size for item in self.content])

    @property
    def abspath(self) -> PurePosixPath:
        return self.path / self.name

    @property
    def _mapping(self) -> dict:
        return {item.name: item for item in self.content}

    def __getitem__(self, key: str) -> Union[File, 'Directory']:
        return self._mapping[key]


def parse_term_output(data: str) -> Directory:
    '''Builds the filesystem representation from terminal output.'''
    path = PurePosixPath('/')
    root_dir = Directory(path=path, name='/', content=[])
    current_dir = root_dir

    for line in data.splitlines():
        args = line.split(' ')
        if args[0] == '$':
            # it's a command.
            if args[1] == 'cd':
                if args[2] == '..':
                    path = path.parent
                    current_dir = current_dir.parent
                else:
                    path = path / args[2]
                    current_dir = root_dir if path.name == '' else current_dir[path.name]

            if args[1] == 'ls':
                # do nothing
                pass
        else:
            if args[0] == 'dir':
                # it's a directory
                item = Directory(path=path, name=args[1], content=[], parent=current_dir)
            else:
                # it's a file
                item = File(path=path, name=args[1], size=int(args[0]), parent=current_dir)
            current_dir.content.append(item)

    return root_dir


def directory_stats(root_dir: Directory) -> List[DirStat]:
    sizes = []

    def dir_sizes(directory):
        sizes.append(DirStat(directory.abspath, directory.size))
        for item in directory.content:
            if type(item) == Directory:
                dir_sizes(item)

    dir_sizes(root_dir)
    return sizes


def fs_counter(data: str):
    file_system = parse_term_output(data)
    fs_stats = directory_stats(file_system)

    yield sum([s.size for s in fs_stats if s.size <= 100000])

    free_space = TOTAL_DISK_SIZE - file_system.size
    assert free_space >= 0

    deletion_size = NEEDED_DISK_SPACE - free_space
    candidates = [s for s in fs_stats if s.size >= deletion_size]
    dir_to_delete = min(candidates, key=lambda x: x.size)

    yield dir_to_delete.size


if __name__ == '__main__':
    test_case = fs_counter(TEST_DATA)
    assert next(test_case) == 95437
    assert next(test_case) == 24933642

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = fs_counter(data)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
