pojson
******

pojson is a tool that allows you to create JSON data files from PO
files. These files are designed to be used with Obviel_'s `i18n support`_.

.. _Obviel: http://obviel.org/

.. _`i18n support`: http://www.obviel.org/en/latest/i18n.html

The `Javascript Gettext`_ already provides a Perl-based tool (po2json)
that is very similar, so this can be seen as a rewrite to Python. One
difference is that pojson does not output domain information in the
resulting datastructure - it is one level less deep. The domain
information must instead be supplied when the file is loaded.

Basic use to generate a JSON file::

  $ pojson <path/to/po> 

Pretty-print output::

  $ pojson -p <path/to/po> 

Help::
  
  $ pojson --help

Normally you would send the output to a file, such as::

  $ pojson something.po > something.json
  
Normally pojson will try to guess the encoding of the .po file, but
you can also explicitly supply an encoding::

  $ pojson -e utf-8 something.po > something.json

_`Javascript Gettext`: http://jsgettext.berlios.de/
