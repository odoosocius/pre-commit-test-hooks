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
    print(directory)
    repo = Repo(directory)
    
    print(repo.remote().fetch(),"is empty")
    for data in repo.remote().fetch():
        print(data.flags)
        print(data.note)
    #print(repo.remotes.origin.fetch("--dry-run"))
    print(repo.git.rev_list("..main"),"revlist")
    #print(repo.git.fetch('origin', '--dry-run'))
    #print(repo.is_dirty(untracked_files=True))
    for remote in repo.remotes:
        print(f'- {remote.name} {remote.url}')
        #print(remote.fetch('--dry-run'),"in loop")
    gg=Git()
    print(gg.fetch('--dry-run'),"is empty")
    print(gg.fetch("origin",dry_run=True),"is empty")
    print(gg.branch(),"is empty")
    result=repo.git.fetch('origin', '--dry-run')
    if result:
        mis_match = True
    return mis_match


def main():
    mis_match = True
    mis_match = check_up_to_date(mis_match)

    return mis_match
