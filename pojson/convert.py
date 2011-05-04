import argh
import simplejson
import polib

def convert(po_file):
    """Convert po_file to dictionary data structure (ready for JSON).
    """
    # XXX encoding?
    po = polib.pofile(po_file, autodetect_encoding=False, encoding='utf-8')

    result = {}

    result['domain'] = domain = {}
    
    domain[''] = po.metadata.copy()

    for entry in po:
        if entry.obsolete:
            continue
        if entry.msgstr:

            domain[entry.msgid] = entry.msgstr
        elif entry.msgstr_plural:
            plural = [entry.msgid_plural]
            domain[entry.msgid] = plural
            ordered_plural = sorted(entry.msgstr_plural.items())
            for order, msgstr in ordered_plural:
                plural.append(msgstr)
    return result

def convert_json(po_file, pretty_print):
    result = convert(po_file)
    if not pretty_print:            
        return simplejson.dumps(result, ensure_ascii=False)
    else:
        return simplejson.dumps(result, sort_keys=True, indent=4 * ' ',
                                ensure_ascii=False)

