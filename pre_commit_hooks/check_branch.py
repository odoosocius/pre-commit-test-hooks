from __future__ import annotations

import argparse
import re
import os.path
from typing import Sequence
import git
from git import Repo


def check_up_to_date():
    
    directory = os.getcwd()
    print(directory)
    repo = Repo(directory)
    g = git.cmd.Git(directory)
    print("this is one option ", g.fetch())
    print(repo)
    print("this is  option two" ,g.fetch('orgin', '--dry-run'))
    result = repo.remote().fetch()
    print(result)
    return True


def main():
    mis_match = True
    mis_match = check_up_to_date()

    return mis_match
