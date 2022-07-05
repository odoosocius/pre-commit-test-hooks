from __future__ import annotations

import os.path
import git
from git import Repo
from git import Git


def check_remote(mis_match):
    g = git.cmd.Git()
    try:
        g.ls_remote('upstream').split('\n')
    except Exception:
        print(
            f'[AUR813].'
            f'You seem not to have an upstream remote'
        )
        mis_match = True
        return mis_match
    if (g.remote('get-url', 'origin') ==
            'https://github.com/odoosocius/TestCodeRepo.git'):
        print(
            f'[FOR813].'
            f'Remote origin is pointing to FernUni'
            f'repository and should be linked to your Fork url'
        )
        mis_match = True
    if (g.remote('get-url', 'upstream') !=
            'https://github.com/odoosocius/TestCodeRepo.git'):
        print(
            f'[FUS813].'
            f'Your upstream remote is '
            f'not the FernUni repository'
        )
        mis_match = True
    return mis_match


def check_up_to_date(mis_match):
    directory = os.getcwd()
    repo = Repo(directory)
    try:
        for data in repo.remote('upstream').fetch("--dry-run"):
            if data.flags != 4 and (data.remote_ref_path).strip() == "main":
                mis_match = True
                print(
                    f'[FD813].'
                    f'Your local repository is not up'
                    f'to date with production repository'
                )
        if repo.git.rev_list("..remotes/upstream/main"):
            mis_match = True
            print(
                f'[FD813].'
                f'Your branch is not up to date with upstream/13.0'
            )
        return mis_match
    except Exception:
        print(
            f'Error'
            f'You seem not to have an upstream remote'
        )
        mis_match = True
        return mis_match

def main():
    mis_match = False
    mis_match = check_remote(mis_match)
    mis_match = check_up_to_date(mis_match)
    return mis_match
