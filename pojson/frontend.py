# -*- coding: utf-8 -*-
import os
try:
    from itertools import izip
except ImportError:
    # for python3
    izip = zip

from distutils import log
from distutils.cmd import Command
from distutils.errors import DistutilsOptionError

from pojson import convert


class po2json(Command):
    """Catalog compilation command for use in ``setup.py`` scripts.

    if target project use old ``distutils``, it needs to explicit register.

        from pojson.frontend import po2json

        setup(
            ...
            cmdclass={'po2json': po2sjon}
        )
    """

    description = 'compile message catalogs(PO files) to JSON files'
    user_options = [
        ('input-files=', 'i',
         'catalogs to compile. separate multiple files with commas(,)'),
        ('output-dir=', 'd',
         'path to output directory'),
        ('pretty-print', 'p',
         'pretty-print JSON output (default False)'),
    ]
    boolean_options = ['pretty-print']

    def initialize_options(self):
        self.input_files = None
        self.output_dir = None
        self.pretty_print = False

    def finalize_options(self):
        if not self.input_files:
            raise DistutilsOptionError('you must specify input files')
        if not self.output_dir:
            raise DistutilsOptionError('you must specify the output directory')

    def run(self):
        po_files = self.input_files.split(",")
        for po_file in po_files:
            if not os.path.isfile(po_file):
                log.error('not a file: {0!r}'.format(po_file))
                continue
            if not po_file.endswith('.po'):
                log.error('not a PO file: {0!r}'.format(po_file))
                continue

            json_file = os.path.normpath(
                os.path.join(self.output_dir,
                             os.path.basename(po_file).replace('.po', '.json'))
            )
            log.info('compiling catalog {0!r} to {1!r}'.format(po_file,
                                                               json_file))

            with open(json_file, "wb") as f:
                f.write(convert(po_file, pretty_print=self.pretty_print)
                        .encode("utf-8"))


class po2json_babel(Command):
    """Catalog compilation command for use in ``setup.py`` scripts.

    if target project use old ``distutils``, it needs to explicit register.

        from pojson.frontend import po2json

        setup(
            ...
            cmdclass={'po2json_babel': po2sjon_babel}
        )

    it's similar to ``po2json`` but has been designed to be compliant with
    catalog structure of ``babel``.
    """

    description = ('compile babel structured message catalogs(PO files) '
                   'to JSON files')
    user_options = [
        ('domain=', 'D',
         "domain of PO file (default 'messages')"),
        ('directory=', 'd',
         'path to base directory containing the catalogs'),
        ('locale=', 'l',
         'locale of the catalog to compile'),
        ('output-dir=', 'o',
         'path to output directory. same as directory if not set'),
        ('pretty-print', 'p',
         'pretty-print JSON output (default False)'),
    ]
    boolean_options = ['pretty-print']

    def initialize_options(self):
        self.domain = 'messages'
        self.directory = None
        self.output_dir = None
        self.locale = None
        self.pretty_print = False

    def finalize_options(self):
        if not self.directory:
            raise DistutilsOptionError('you must specify the base directory')

        if not self.output_dir:
            self.output_dir = self.directory

    def run(self):
        po_files = []
        json_files = []

        if self.locale:
            po_files.append(os.path.join(self.directory, self.locale,
                                         'LC_MESSAGES',
                                         self.domain + '.po'))
            json_files.append(os.path.join(self.output_dir, self.locale,
                                           'LC_MESSAGES',
                                           self.domain + '.json'))
        else:
            for locale in os.listdir(self.directory):
                po_file = os.path.join(self.directory, locale,
                                       'LC_MESSAGES', self.domain + '.po')

                if os.path.exists(po_file):
                    po_files.append(po_file)
                    json_files.append(os.path.join(self.output_dir, locale,
                                                   'LC_MESSAGES',
                                                   self.domain + '.json'))

        if not po_files:
            raise DistutilsOptionError('no message catalogs found')

        for po_file, json_file in izip(po_files, json_files):
            log.info('compiling catalog {0!r} to {1!r}'.format(po_file,
                                                               json_file))

            output_dir = os.path.dirname(json_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            with open(json_file, "wb") as f:
                f.write(convert(po_file, pretty_print=self.pretty_print)
                        .encode("utf-8"))
