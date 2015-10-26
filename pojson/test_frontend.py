# -*- coding: utf-8 -*-

import os

from distutils.dist import Distribution
from distutils.errors import DistutilsOptionError

from pytest import raises

from pojson.convert import convert
from pojson.frontend import po2json, po2json_babel

from pojson import PY3K


def pytest_funcarg__po2json(request):
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


def test_po2json_without_input_files(po2json):
    with raises(DistutilsOptionError):
        po2json.finalize_options()


def test_po2json_without_output_dir(po2json, input_file):
    po2json.input_files = input_file
    with raises(DistutilsOptionError):
        po2json.finalize_options()


def check_po_to_json(po_file, output_dir):
    json_file = os.path.normpath(
        os.path.join(output_dir,
                     os.path.basename(po_file).replace('.po', '.json')))
    assert os.path.isfile(json_file)

    try:
        with open(json_file) as f:
            if PY3K:
                assert f.read() == convert(po_file)
            else:
                assert f.read() == convert(po_file).encode("utf-8")
    finally:
        os.unlink(json_file)


def test_po2json_single_file(po2json, input_file, output_dir):
    po2json.input_files = input_file
    po2json.output_dir = output_dir

    po2json.finalize_options()
    po2json.run()
    check_po_to_json(input_file, output_dir)


def test_po2json_multiple_file(po2json, input_files, output_dir):
    po2json.input_files = input_files
    po2json.output_dir = output_dir

    po2json.finalize_options()
    po2json.run()
    for po_file in input_files.split(','):
        check_po_to_json(po_file, output_dir)


def pytest_funcarg__po2json_babel(request):
    dist = Distribution(dict(
        name='TestProject',
        version='0.1',
        packages=['project']
    ))
    cmd = po2json_babel(dist)
    cmd.initialize_options()
    return cmd


def pytest_funcarg__directory(request):
    return os.path.join(
        os.path.dirname(request.module.__file__), 'testdata', 'babel_messages')


def test_po2json_babel_without_input_files(po2json_babel):
    with raises(DistutilsOptionError):
        po2json_babel.finalize_options()


def test_po2json_babel(po2json_babel, directory):
    po2json_babel.directory = directory

    po2json_babel.finalize_options()
    po2json_babel.run()
    for locale in os.listdir(directory):
        message_dir = os.path.join(directory, locale, 'LC_MESSAGES')
        po_file = os.path.join(message_dir, 'messages.po')
        check_po_to_json(po_file, message_dir)


def test_po2json_babel_with_output_dir(po2json_babel, directory, output_dir):
    po2json_babel.directory = directory
    po2json_babel.output_dir = output_dir

    po2json_babel.finalize_options()
    po2json_babel.run()
    for locale in os.listdir(directory):
        message_dir = os.path.join(directory, locale, 'LC_MESSAGES')
        output_dir_ = os.path.join(output_dir, locale, 'LC_MESSAGES')
        po_file = os.path.join(message_dir, 'messages.po')
        check_po_to_json(po_file, output_dir_)
