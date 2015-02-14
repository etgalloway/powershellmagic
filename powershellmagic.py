"""IPython magics for Windows PowerShell.
"""
__version__ = '0.1'

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
    """
    # This class is patterned after
    # IPython.core.magics.script.ScriptMagics.

    def __init__(self, shell=None):
        super(PowerShellMagics, self).__init__(shell=shell)
        tf = tempfile.NamedTemporaryFile(suffix='.ps1', delete=False)
        self._input_file_name = tf.name
        atexit.register(self._delete_powershell_input_file)

    def _delete_powershell_input_file(self):
        """Delete PowerShell input file."""
        os.remove(self._input_file_name)

    @magic_arguments()
    @argument(
        '--out',
        type=str,
        help="Redirect stdout to a variable."
        )
    @argument(
        '--err',
        type=str,
        help="Redirect stderr to a variable."
        )
    @cell_magic
    def powershell(self, line, cell):
        """Execute a cell written in PowerShell by spawning a process
        that invokes the command:

           PowerShell -ExecutionPolicy RemoteSigned -File tempfile.ps1

        where the argument to '-File' is a file that contains the contents
        of the cell.
        """
        # This function is patterned after
        # IPython.core.magics.ScriptMagics.shebang.

        args = parse_argstring(self.powershell, line)

        with open(self._input_file_name, mode='w') as f:
            f.write(cell)

        cmd = 'PowerShell -ExecutionPolicy RemoteSigned -File {}\r\n'
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
