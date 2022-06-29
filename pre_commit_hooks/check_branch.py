from __future__ import annotations

import argparse
import re
import os.path
from typing import Sequence
import git
from git import Repo
from git import Git


def check_up_to_date(mis_match):
    
    directory = os.getcwd()
    repo = Repo(directory)
    for data in repo.remote().fetch("--dry-run"):
        print(data.flags)
        print(data.ref)
        print(data.remote_ref_path)
        if data.flags!=4 and data.remote_ref_path =="main":
            mis_match = True
    if repo.git.rev_list("..main"):
        mis_match = False
    return mis_match


def main():
    mis_match = False
    mis_match = check_up_to_date(mis_match)

    return mis_match
