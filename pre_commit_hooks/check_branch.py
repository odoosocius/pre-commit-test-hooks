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
        if data.flags!=4 and data.remote_ref_path =="main":
            mis_match = True
             print(
                    f'[FD813].'
                    f'branch  is not up to date .'  
                )
    if repo.git.rev_list("..main"):
        mis_match = True
        print(
                    f'[FD813].'
                    f'branch is not up to date .'  
                )
    return mis_match


def main():
    mis_match = False
    mis_match = check_up_to_date(mis_match)

    return mis_match
