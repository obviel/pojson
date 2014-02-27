# -*- coding: utf-8 -*-
import os

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
