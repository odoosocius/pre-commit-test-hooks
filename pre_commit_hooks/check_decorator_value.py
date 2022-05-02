from __future__ import annotations
from typing import Sequence
import argparse
import re
import os.path



def check_decorator(src, filename: str = '<unknown>') -> int:
    file = src.readlines()
    missing_tag = False
    lastline = ""
    for line in file:
        if re.search("^class.*:$", line):
            print(lastline)
            if (
                lastline == ""
                or ('funid_test' not in lastline )
            ):
                index = file.index(line)
                print(
                    f'{filename}:  missing tag "funid_test"'
                    f'(on line {index}).',
                )
                missing_tag = True
                break
        lastline = line
        # print(lastline)
    return missing_tag


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--django', default=False, action='store_true',
        help='Use Django-style test naming pattern (test*.py)',
    )
    args = parser.parse_args(argv)
    retval = 0
    test_name_pattern = r'test.*\.py' if args.django else r'.*_test\.py'
    for filename in args.filenames:
        base = os.path.basename(filename)
        print("this is base ",base)
        print(filename)
        if (
                re.match(test_name_pattern, base) and
                not base == '__init__.py' 
        ):
            print(filename)
            with open(filename, 'rb') as f:
                retval = check_decorator(f, filename=filename)
    return True
