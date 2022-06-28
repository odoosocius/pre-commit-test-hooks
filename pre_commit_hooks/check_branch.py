from __future__ import annotations

import argparse
import re
import os.path
from typing import Sequence
import git
from git import Repo


def check_up_to_date_with_cloud(mis_match):
    
    git = repo.git
    print(git)
    print("will this work",git.fetch('origin', '--dry-run'))
    result = git.fetch('origin', '--dry-run')
    
    if result:
        print("is not uptodate with cloned repo ")
        mis_match = True
    return mis_match



def main():
    mis_match = True
    mis_match = check_up_to_date_with_cloud(mis_match)

    return mis_match
