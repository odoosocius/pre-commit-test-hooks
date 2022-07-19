from __future__ import annotations

import argparse
import re
import os.path
import ast
from lxml import etree
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

DFTL_VALID_ODOO_VERSIONS = ['15.0',
                            ]



def check_field_selection_add(filename, condition_failed):
    """Function to check py file contain selection add"""
    print("using enumarator")
    print(filename)
    selection_start = False
    selection_add = False
    ondelete = False
    lineno = 0
    found_line = False
    with open(filename, 'r') as fp:
        for l_no, line in enumerate(fp):
            if selection_start and found_line != line:
                if line == '' or 'fields' in line and not ondelete:
                    print(
                        f'[SF814].'
                        f'{filename}: {lineno} selection_add '
                        f' does not contain ondelete'
                    )
                    condition_failed =True
                    selection_add =False
                    selection_start = False
                    ondelete = False
            if 'fields.Selection'in line:
                selection_start = True
                lineno = l_no
                found_line = line
            if selection_start and 'selection_add=[' in line:
                selection_add = True
               
            if selection_start and selection_add and found_line == line:
                if 'ondelete' not in line:
                    continue
            


    return condition_failed


def check_migration_folder(dir_list, condition_failed):
    """checks if the uploded module has migration folder
    Returns: The value condition_failed = true if module hs
    migration folder
    """
    for directory in dir_list:
        path = os.getcwd() + '/' + directory
        for path in os.listdir(path):
            if path == 'migrations':
                condition_failed = True
                print(
                    f'[MF813].'
                    f'{directory} contain migration folder '
                    f'No migrations folder should be included '
                    f'in any changed files'
                )
    return condition_failed


def version_check(filename, condition_failed):
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


def parse_xml(xml_file, raise_if_error=False):
    """Get xml parsed.
    :param xml_file: Path of file xml
    :return: Doc parsed (lxml.etree object)
        if there is syntax error return string error message
    """
    if not os.path.isfile(xml_file):
        return etree.Element("__empty__")
    try:
        with open(xml_file, "rb") as f_obj:
            doc = etree.parse(f_obj)
    except etree.XMLSyntaxError as xmlsyntax_error_exception:
        if raise_if_error:
            raise xmlsyntax_error_exception
        return etree.Element("__empty__")
    return doc


def get_xml_records(xml_file, model=None, more=None):
    """Get tag `record` of a openerp xml file.
    :param xml_file: Path of file xml
    :param model: String with record model to filter.
                if model is None then get all.
                Default None.
    :return: List of lxml `record` nodes
        If there is syntax error return []
    """
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
    return doc


def check_traw(xml_file, condition_failed):
    """Function to check if the xml contains t-raw or not """
    deprecated_directives = {
        't-raw',
    }
    directive_attrs = '|'.join('@%s' % d for d in deprecated_directives)
    # checking for pattern
    xpath = '|'.join(
        '/%s//template//*[%s]' % (tag, directive_attrs)
        for tag in ('odoo', 'openerp')
    )

    doc = get_xml_records(xml_file)
    for node in doc.xpath(xpath):
        directive = next(
            iter(set(node.attrib) & deprecated_directives))
        if directive:
            condition_failed = True
            print(
                f'[WF813].'
                f'{xml_file}: {node.sourceline} contain t-raw,'
                f' T-Raw has been replaced by '
                f'T-OUT or T-ESC'
            )
    return condition_failed


def check_invisible_readonly(xml_file, condition_failed):
    """check if view contain invisible or readonly without attrs"""
    deprecated_directives = {
        'readonly',
        'invisible',
    }
    directive_attrs = '|'.join('@%s' % d for d in deprecated_directives)
    xpath = '|'.join(
        '/%s//*[%s]' % (tag, directive_attrs)
        for tag in ('odoo', 'openerp')
    )
    doc = get_xml_records(xml_file)
    print("doc in invisible", doc)
    for node in doc.xpath(xpath):
        directive = next(
            iter(set(node.attrib) & deprecated_directives))
        if directive:
            condition_failed = True
            print(
                f'[WF814].'
                f'{xml_file}: {node.sourceline} contain {directive},'
                f' ‘invisible’ and ‘readonly’ should be used with ‘attrs’'
            )

    return condition_failed


def main(argv: Sequence[str] | None = None) -> int:
    condition_failed = True

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    dir_list = []
    for filename in args.filenames:
        # os.path.basename to get path
        file_name = os.path.basename(filename)
        # search for files that end with .xml
        if (
                re.search("[\w.-]xml$", file_name)):
            condition_failed = check_traw(filename, condition_failed)
            condition_failed = check_invisible_readonly(
                filename, condition_failed)
        if (
                re.search("[\w.-]py$", file_name)):
                condition_failed = check_field_selection_add(filename, condition_failed)

        #  checks for manifest  file
        is_manifest = file_name in MANIFEST_FILES
        if is_manifest:
            condition_failed = version_check(filename, condition_failed)
        dir1 = os.path.dirname(filename).split('/')
        if dir1[0] != '':
            dir_list.append(dir1[0])
    dir_list = set(dir_list)
    condition_failed = check_migration_folder(dir_list, condition_failed)
    return condition_failed
