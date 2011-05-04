import argh
import pojson

@argh.arg('-p', '--pretty-print', default=False, help="Pretty-print JSON")
@argh.arg('-e', '--encoding', default=None, help="Encoding of PO file")
@argh.arg('-j', '--javascript', default=False, help="Generate JS instead of JSON")
@argh.arg('domain', help='Translation domain')
@argh.arg('po_file', help='PO file')
def convert(args):
    print pojson.convert(args.domain,
                         args.po_file,
                         js=args.javascript,
                         encoding=args.encoding,
                         pretty_print=args.pretty_print).encode('utf-8')

def main():
    p = argh.ArghParser()
    p.add_commands([convert])
    p.dispatch()
