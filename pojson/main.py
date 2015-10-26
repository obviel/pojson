import argparse
import pojson
import os
from . import PY3K


def main():
    p = argparse.ArgumentParser(description='convert .po to .json')
    p.add_argument('po_file')
    p.add_argument('-e', '--encoding', help='encoding of po file')
    p.add_argument('-p', '--pretty-print', help='pretty-print JSON output',
                   action="store_true")
    args = p.parse_args()

    if not os.path.isfile(args.po_file):
        p.exit(u"not a file: %s" % args.po_file)
    if not args.po_file.endswith('.po'):
        p.exit(u"not a PO file: %s" % args.po_file)

    if PY3K:
        print(pojson.convert(
            args.po_file, encoding=args.encoding,
            pretty_print=args.pretty_print))
    else:
        print(pojson.convert(
            args.po_file, encoding=args.encoding,
            pretty_print=args.pretty_print).encode('utf-8'))
