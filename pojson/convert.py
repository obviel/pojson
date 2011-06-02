import argh
import simplejson
import polib
import os

def po2dict(po):
    """Convert po object to dictionary data structure (ready for JSON).
    """
    result = {}
    
    result[''] = po.metadata.copy()

    for entry in po:
        if entry.obsolete:
            continue
        if entry.msgstr:
            result[entry.msgid] = [None, entry.msgstr]
        elif entry.msgstr_plural:
            plural = [entry.msgid_plural]
            result[entry.msgid] = plural
            ordered_plural = sorted(entry.msgstr_plural.items())
            for order, msgstr in ordered_plural:
                plural.append(msgstr)
    return result

def convert(domain, po_file, js=False, encoding=None, pretty_print=False):
    if not os.path.isfile(po_file):
        raise argh.exceptions.CommandError(u"Not a file: %s" % po_file)
    if not po_file.endswith('.po'):
        raise argh.exceptions.CommandError(u"Not a PO file: %s" % po_file)
    if encoding is None:
        po = polib.pofile(po_file,
                          autodetect_encoding=True)
    else:
        po = polib.pofile(po_file,
                          autodetect_encoding=False,
                          encoding=encoding)
    
    domain_data = po2dict(po)
    
    d = { domain: domain_data }
    if not pretty_print:
        result = simplejson.dumps(d, ensure_ascii=False, sort_keys=True)
    else:
        result = simplejson.dumps(d, sort_keys=True, indent=4 * ' ',
                                  ensure_ascii=False)
    if js:
        result = 'var json_locale_data = ' + result + ';'
    return result

        
