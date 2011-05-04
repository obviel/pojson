import argh
import pojson

@argh.arg('-p', '--pretty-print', default=False, help="Pretty-print JSON")
@argh.arg('po_file')
def convert(args):
    print pojson.convert_json(args.po_file, args.pretty_print).encode('utf-8')

def main():
    p = argh.ArghParser()
    p.add_commands([convert])
    p.dispatch()
