#!/usr/bin/env python3

import hashlib
import argparse
import os
import sys
import pytablewriter

def get_hashes_for_files_in_path(path):
    results = []
    for file in sorted([f for f in [os.path.join(path, f) for f in os.listdir(path)] if os.path.isfile(f)]):
        with open(file, 'rb') as f:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            while True:
                buf = f.read(4096)
                if not buf:
                    break
                md5.update(buf)
                sha1.update(buf)
            results.append([file, md5.hexdigest(), sha1.hexdigest() ])
    return results

def main():
    parser = argparse.ArgumentParser(
        prog='hashreport',
        description='Print MD5 and SHA1 checksums in a Markdown table.')
    parser.add_argument('input', metavar='INPUT', type=str, help='path to a directory of files to hash')
    parser.add_argument('--version', action='version', version='%(prog)s v0.1')

    args = parser.parse_args()
    hashes = get_hashes_for_files_in_path(args.input)
    writer = pytablewriter.MarkdownTableWriter(
        headers=["File", "MD5", "SHA1"],
        value_matrix=hashes,
        margin=1)
    writer.write_table()

if __name__ == "__main__":
    main()