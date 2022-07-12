from __future__ import annotations

import argparse
import re
import os.path
import ast
import astroid
from distutils.version import LooseVersion
from pathlib import Path
from typing import Sequence

MANIFEST_FILES = [
    '__manifest__.py',
    '__odoo__.py',
    '__openerp__.py',
    '__terp__.py',
]

odoo_check_versions = {
            'name_check': {
                'min_odoo_version': '15.0',
                'max_odoo_version': '15.0',
            }
        }

DFTL_VALID_ODOO_VERSIONS = [ '15.0',
]

def check_migration_folder(dir_list,condition_failed):
    """checks if the uploded module has migration folder
    Returns: The value condition_failed = true if module hs 
    migration folder  
    """
    for directory in dir_list:
        path = os.getcwd()+'/'+directory
        for path in os.listdir(path):
            condition_failed = True
            if path =='migrations':
                print(
                    f'[MF813].'
                    f'{directory} contain migration folder '
                    f'No migrations folder should be included '
                    f'in any changed files'
                )
    return condition_failed


def version_check(filename,condition_failed):
    with open(filename) as f_manifest:
        manifest_dict = ast.literal_eval(f_manifest.read())
        version = manifest_dict.get("version")
        check_versions = odoo_check_versions.get("name_check", {})
        min_odoo_version = check_versions.get(
            'min_odoo_version')
        if version < min_odoo_version:
            print(
                    f'[MV813].'
                    f'{filename}: contain version less than 15.0'
                    f' the version of module should be greater than "15.0"'
            )


# def



def main(argv: Sequence[str] | None = None) -> int:
    condition_failed = True
    # condition_failed = check_migration_folder(condition_failed)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    asfrgss = (getattr(parser, 'args', None) or []) + \
        (getattr(parser, 'keywords', None) or [])
    print(asfrgss)
    dir_list = []
    for filename in args.filenames:
        file_name = os.path.basename(filename)
        is_manifest = file_name in MANIFEST_FILES
        if is_manifest:
            condition_failed = version_check(filename,condition_failed)
        dir1 = os.path.dirname(filename).split('/')
        if dir1[0] != '':
            dir_list.append(dir1[0])
    dir_list = set(dir_list)
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
