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
    g = git.cmd.Git(directory)
    result = g.fetch('origin', '--dry-run')
    print(g.pul(),"pull request")
    print(result,"this is the result")
    if result:
        mis_match = True
    return mis_match


def main():
    mis_match = True
    mis_match = check_up_to_date(mis_match)

    return mis_match
