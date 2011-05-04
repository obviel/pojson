pojson
******

pojson is a tool that allows you to create JSON data (and .js) files
from PO files. The JSON and .js files are compatible with the format
required by `Javascript Gettext`_. It can be used instead of the
Perl-based po2json tool included in this project.

Basic use::

  $ pojson convert <translation_domain> <path/to/po> 

Generate .js file::

  $ pojson convert -j <translation_domain> <path/to/po>

Pretty-print output::

  $ pojson convert -p <translation_domain> <path/to/po> 

Help::
  
  $ pojson convert --help

Normally you would send the output to a file, such as::

  $ pojson convert myproject something.po > something.json
  
  $ pojson convert -j myproject something.po > something.js

Normally pojson will try to guess the encoding of the .po file, but
you can also explicitly supply an encoding::

  $ pojson convert -e utf-8 myproject something.po > something.json

_`Javascript Gettext`: http://jsgettext.berlios.de/
