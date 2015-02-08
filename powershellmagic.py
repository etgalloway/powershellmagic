"""IPython magics for Windows PowerShell.
"""

import atexit
import os
from subprocess import Popen, PIPE
import sys
import tempfile

from IPython.core.magic import (cell_magic, Magics, magics_class)
from IPython.core.magic_arguments import (
    argument, magic_arguments, parse_argstring)


@magics_class
class PowerShellMagics(Magics):
    """IPython magics class for Windows PowerShell.

    This class is patterned after IPython.core.magics.script.ScriptMagics.
    """

    def __init__(self, shell=None):
        super(PowerShellMagics, self).__init__(shell=shell)
        tf = tempfile.NamedTemporaryFile(suffix='.ps1', delete=False)
        self._input_file_name = tf.name
        atexit.register(self._delete_powershell_input_file)

    def _delete_powershell_input_file(self):
        """Delete PowerShell input file."""
        os.remove(self._input_file_name)

    @magic_arguments()
    @argument('--out', type=str)
    @argument('--err', type=str)
    @cell_magic
    def powershell(self, line, cell):
        """Execute a cell body using Powershell.

        This function is patterned after
        IPython.core.magics.ScriptMagics.shebang.
        """

        args = parse_argstring(self.powershell, line)

        with open(self._input_file_name, mode='w') as f:
            f.write(cell)

        cmd = 'powershell -ExecutionPolicy RemoteSigned -File {}\r\n'
        cmd = cmd.format(self._input_file_name)

        p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
        out, err = p.communicate()

        out = out.decode()
        err = err.decode()

        if args.out:
            self.shell.user_ns[args.out] = out
        else:
            sys.stdout.write(out)
            sys.stdout.flush()

        if args.err:
            self.shell.user_ns[args.err] = err
        else:
            sys.stderr.write(err)
            sys.stderr.flush()


def load_ipython_extension(ip):
    """Load PowerShellMagics extension"""
    ip.register_magics(PowerShellMagics)
