from __future__ import annotations

import argparse
import re
import os.path
from typing import Sequence
import git
from git import Repo


def check_up_to_date_with_cloud(mis_match):
    
    directory = os.getcwd()
    print(directory)
    repo = Repo(directory)
    print(repo)
    print("will this work",git.fetch('origin', '--dry-run'))
    g = git.cmd.Git(directory)
    print(g.fetch('origin', '--dry-run'),"this is results")
    result = g.fetch('origin', '--dry-run')
    print("is not uptodate with cloned repo ")
    if result:
        mis_match = True
    return mis_match



def main():
    mis_match = True
    mis_match = check_up_to_date_with_cloud(mis_match)
    mis_match = check_up_to_date_with_local_repo(mis_match)

    return mis_match
