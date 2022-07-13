from __future__ import annotations

import argparse
import re
import os.path
import ast
from lxml import etree
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
            if path =='migrations':
                condition_failed = True
                print(
                    f'[MF813].'
                    f'{directory} contain migration folder '
                    f'No migrations folder should be included '
                    f'in any changed files'
                )
    return condition_failed

def parse_xml(xml_file, raise_if_error=False):
    """Get xml parsed.
    :param xml_file: Path of file xml
    :return: Doc parsed (lxml.etree object)
        if there is syntax error return string error message
    """
    if not os.path.isfile(xml_file):
        print("failed here")
        return etree.Element("__empty__")
    try:
        with open(xml_file, "rb") as f_obj:
            doc = etree.parse(f_obj)
    except etree.XMLSyntaxError as xmlsyntax_error_exception:
        print("error occured")
        if raise_if_error:
            raise xmlsyntax_error_exception
        return etree.Element("__empty__")
    print("am i seeing things",)
    return doc

def version_check(filename,condition_failed):
    """ checking if version is less than 15.0"""
    with open(filename) as f_manifest:
        manifest_dict = ast.literal_eval(f_manifest.read())
        # returns manifest as dict 
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
            condition_failed = True
    return condition_failed
        

def get_xml_records(xml_file, model=None, more=None):
    """Get tag `record` of a openerp xml file.
    :param xml_file: Path of file xml
    :param model: String with record model to filter.
                if model is None then get all.
                Default None.
    :return: List of lxml `record` nodes
        If there is syntax error return []
    """
    deprecated_directives = {
        't-raw',
    }
    directive_attrs = '|'.join('@%s' % d for d in deprecated_directives)
    xpath = '|'.join(
        '/%s//template//*[%s]' % (tag, directive_attrs)
        for tag in ('odoo', 'openerp')
    )

    if not xml_file:
        return []
    if model is None:
        model_filter = ''
    else:
        model_filter = "[@model='{model}']".format(model=model)
    if more is None:
        more_filter = ''
    else:
        more_filter = more
    doc = parse_xml(xml_file)
    # root = etree.fromstring(doc, etree.HTMLParser())
    print("is doc" ,doc)
    for node in doc.xpath(xpath):
        print(node)
        directive = next(
            iter(set(node.attrib) & deprecated_directives))
        print(directive)
    # print(etree.fromstring(doc, etree.HTMLParser()))
    # return doc.xpath("/openerp//record" + model_filter + more_filter) + \
    #     doc.xpath("/odoo//record" + model_filter + more_filter)
    # print(doc.xpath("/openerp//record" + model_filter + more_filter) + doc.xpath("/odoo//record" + model_filter + more_filter))


def check_traw(xml_file):
    get_xml_records(xml_file)

    





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
        if (
                re.search("[\w.-]xml$", file_name)):
            check_traw(filename,)

        is_manifest = file_name in MANIFEST_FILES
        if is_manifest:
            condition_failed = version_check(filename,condition_failed)
        dir1 = os.path.dirname(filename).split('/')
        if dir1[0] != '':
            dir_list.append(dir1[0])
    dir_list = set(dir_list)
    # condition_failed = check_migration_folder(dir_list,condition_failed)


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
