from __future__ import annotations

import argparse
import re
import os.path
import ast
from pathlib import Path
from typing import Sequence

MANIFEST_FILES = [
    '__manifest__.py',
    '__odoo__.py',
    '__openerp__.py',
    '__terp__.py',
]


def check_migration_folder(dir_list,condition_failed):
    """checks if the uploded module has migration folder
    Returns: The value condition_failed = true if module hs 
    migration folder  
    """
    for directory in dir_list:
        print(directory)
        path = os.getcwd()+'/'+directory
        print(os.getcwd()+'/'+directory+'/'+'migrations')
        for path in os.listdir(path):
            condition_failed = True
            if path=='migrations':
                print(
            f'[MF813].'
            f'No migrations folder should be included in any changed files'
        )   
    return condition_failed

def version_check(filename,condition_failed):
    with open(filename) as f_manifest:
        manifest_dict = ast.literal_eval(f_manifest.read())
        print(manifest_dict)



def main(argv: Sequence[str] | None = None) -> int:
    condition_failed = True
    # condition_failed = check_migration_folder(condition_failed)
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    dir_list = []
    for filename in args.filenames:
        file_name = os.path.basename(filename)
        is_manifest = file_name in MANIFEST_FILES
        if is_manifest:
            condition_failed = version_check(filename,condition_failed)
        print("is working",is_manifest)
        dir1 = os.path.dirname(filename).split('/')
        if dir1[0] != '':
            dir_list.append(dir1[0])
#         dir_list.append(dir)
    print(dir_list)
    dir_list  = set(dir_list)
    condition_failed = check_migration_folder(dir_list,condition_failed)


        # if '' in dir:
        #     base = os.path.basename(filename)
        #     if (
        #             re.match("^test.*py$", base) or
        #             base == 'common.py'
        #     ):
        #         with open(filename, 'rb') as f:
        #             missing_tag = check_decorator(
        #                 f, missing_tag, filename=filename
        #             )
    return condition_failed
