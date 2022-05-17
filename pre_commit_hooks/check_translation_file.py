from __future__ import annotations
import argparse
import polib
import os.path
import re
from typing import Sequence
from collections import Counter


def emptypo():
    po_obj = polib.POFile()
    po_obj.metadata = {
        "Project-Id-Version": "Odoo Server 13.0+e",
        "Report-Msgid-Bugs-To": "",
        "POT-Creation-Date": "2020-03-26 15:18+0000",
        "PO-Revision-Date": "2020-03-26 15:18+0000",
        "Last-Translator": "",
        "Language-Team": "",
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "",
        "Plural-Forms": "",
    }
    return po_obj


def searchDuplicates(po_file_path, duplicate,filename):
    """
    Log all those msgid duplicated inside the file
    """
    duplicate = duplicate
    po_file = po_file_path
    msg_ids = [entry.msgid for entry in po_file]
    test = [ entry for entry in po_file ]
    print(test)
    counter_dict = Counter(msg_ids)
    if any(el for el in counter_dict.values() if el > 1):
        print("[DT8013] Follwing Duplicates Terms are found! on file ",filename)
        duplicate = True
    for key, value in counter_dict.items():
        if value > 1:
            print(key,",")         
    return duplicate


def sort_entries(po_file_path, duplicate, save=False):
    """
    Sort a po file
    :rtype: object
    """
    po_sorted = polib.POFile()
    po_file = polib.pofile(po_file_path)
    po_out = emptypo()
    po_sorted = polib.POFile()
    for entry in sorted(po_file, key=lambda x: x.msgid):
        po_out.append(entry)
        po_sorted.append(entry)
    if po_out != po_file and save:
        file_name = po_file_path
        print("[FS8013] File Sorted", file_name)
        po_out.save(file_name)
        searchDuplicates(po_sorted,duplicate,po_file_path)
        return True
    return searchDuplicates(po_sorted,duplicate,po_file_path)
    

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    duplicate = False
    for filename in args.filenames:
        base = os.path.basename(filename)
        if (re.search(".po$", base)):
            duplicate = sort_entries(filename,duplicate,True)
            
    return true


if __name__ == "__main__":
    raise SystemExit(main())


# f = open("/home/socius/fr_CH.po", "r")
# file = f.read()
# sortEntries('/home/socius/fr_CH.po',False,True)
