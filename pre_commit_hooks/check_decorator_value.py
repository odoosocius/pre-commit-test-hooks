from __future__ import annotations

import argparse
import re
import io
import os.path
import tokenize
from tokenize import tokenize as tokenize_tokenize
from typing import Sequence



def check_decorator(src: bytes, filename: str = '<unknown>') -> int:
    file = src.readlines()
    missing_tag = False
    lastline = ""
    print(file)
    print(file.decode("utf-8"))
    print(tokenize_tokenize(file))
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
    print(args.filenames)
    retval = 0
    for filename in args.filenames:
        base = os.path.basename(filename)
        print("this is base ",base)
        print(filename)
        print(re.match("^test.*py$", base))
        if (
                re.match("^test.*py$", base) and
                base != '__init__.py' 
        ):
            print(filename)
            with open(filename, 'rb') as f:
                retval = check_decorator(f, filename=filename)
    return True
