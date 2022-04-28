from __future__ import annotations
import argparse
import io
import re
import tokenize
from tokenize import tokenize as tokenize_tokenize
from typing import Sequence


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
    args = parser.parse_args(argv)
    retval = 0
    for filename in args.filenames:
        with open(filename, 'rb') as f:
            retval = check_decorator(f, filename=filename)
    return retval

if __name__ == "__main__":
    raise SystemExit(main())