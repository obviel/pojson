# -*- coding: utf-8 -*-

import os

from distutils.dist import Distribution
from distutils.errors import DistutilsOptionError

from pytest import raises

from pojson.convert import convert
from pojson.frontend import po2json


def pytest_funcarg__cmd(request):
    dist = Distribution(dict(
        name='TestProject',
        version='0.1',
        packages=['project']
    ))
    cmd = po2json(dist)
    cmd.initialize_options()
    return cmd


def pytest_funcarg__input_file(request):
    return os.path.join(
        os.path.dirname(request.module.__file__), 'testdata', 'nl.po')


def pytest_funcarg__input_files(request):
    return ','.join([
        os.path.join(
            os.path.dirname(request.module.__file__), 'testdata', 'nl.po'),
        os.path.join(
            os.path.dirname(request.module.__file__), 'testdata', 'ko.po')
    ])


def pytest_funcarg__output_dir(request):
    return os.path.dirname(request.module.__file__)


def test_po2json_without_input_files(cmd):
    with raises(DistutilsOptionError):
        cmd.finalize_options()


def test_po2json_without_output_dir(cmd, input_file):
    cmd.input_files = input_file
    with raises(DistutilsOptionError):
        cmd.finalize_options()


def check_po_to_json(po_file, output_dir):
    json_file = os.path.normpath(
        os.path.join(output_dir,
                     os.path.basename(po_file).replace('.po', '.json')))
    assert os.path.isfile(json_file)

    try:
        with open(json_file) as f:
            assert f.read() == convert(po_file).encode("utf-8")
    finally:
        os.unlink(json_file)


def test_po2json_single_file(cmd, input_file, output_dir):
    cmd.input_files = input_file
    cmd.output_dir = output_dir

    cmd.finalize_options()
    cmd.run()
    check_po_to_json(input_file, output_dir)


def test_po2json_multiple_file(cmd, input_files, output_dir):
    cmd.input_files = input_files
    cmd.output_dir = output_dir

    cmd.finalize_options()
    cmd.run()
    for po_file in input_files.split(','):
        check_po_to_json(po_file, output_dir)
