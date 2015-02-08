"""Tests for PowerShellMagic.

   Usage:
     $ nosetests test_powershellmagic.py

"""
import IPython
import nose
import sys

if sys.version_info.major == 2:
    from StringIO import StringIO
else:
    from io import StringIO

if sys.version_info >= (3, 3):
    from unittest import mock
else:
    import mock


if not IPython.get_ipython():
    from IPython.testing import globalipapp
    globalipapp.start_ipython()

ip = IPython.get_ipython()


def setup():
    ip.extension_manager.load_extension('powershellmagic')


def test_powershell_no_flags():
    cell = "echo hello"
    with mock.patch("sys.stdout", StringIO()) as out:
        ip.run_cell_magic("powershell", "", cell)
    nose.tools.assert_equal(out.getvalue(), "hello\r\n")


def test_powershell_out():
    cell = "echo hello"
    ip.run_cell_magic("powershell", '--out output', cell)
    nose.tools.assert_equal(ip.user_ns['output'], "hello\r\n")


def test_powershell_err():
    cell = "$host.ui.WriteErrorLine('hello')"
    ip.run_cell_magic("powershell", '--err error', cell)
    nose.tools.assert_equal(ip.user_ns['error'], "hello\r\n")


def test_powershell_out_err():
    cell = "echo hello\n" + "$host.ui.WriteErrorLine('hi')"
    ip.run_cell_magic("powershell", '--out output --err error', cell)
    nose.tools.assert_equal(ip.user_ns['output'], 'hello\r\n')
    nose.tools.assert_equal(ip.user_ns['error'], 'hi\r\n')
