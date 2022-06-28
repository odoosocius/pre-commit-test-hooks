from __future__ import annotations

import argparse
import re
import os.path
from typing import Sequence
import git
from git import Repo


def check_up_to_date(mis_match):
    
    directory = os.getcwd()
    print(directory)
    repo = Repo(directory)
    print(repo)
    o = repo.remotes.origin
    print(o.fetch('origin', '--dry-run'))
    result=o.fetch('origin', '--dry-run')
    if result:
        mis_match = True
    return mis_match


def main():
    mis_match = True
    mis_match = check_up_to_date(mis_match)

    return mis_match
