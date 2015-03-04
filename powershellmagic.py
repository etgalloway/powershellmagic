"""IPython magics for Windows PowerShell.
"""
__version__ = '0.1.0'

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
        self._cell_file_name = self._powershell_tempfile()

    def _powershell_tempfile(self):
        tf = tempfile.NamedTemporaryFile(suffix='.ps1', delete=False)
        atexit.register(self._delete_powershell_tempfile)
        return tf.name

    def _delete_powershell_tempfile(self):
        os.remove(self._cell_file_name)

    @magic_arguments()
    @argument(
        '--out',
        type=str,
        help="Redirect cell stdout to a variable."
        )
    @argument(
        '--err',
        type=str,
        help="Redirect cell stderr to a variable."
        )
    @cell_magic
    def powershell(self, line, cell):
        """Use Windows PowerShell to execute an IPython cell.

        An example:

            In [1]: %%powershell
               ...: foreach ($i in 1..3) {
               ...:    $i
               ...: }
               ...:
            1
            2
            3

        """
        # This function is patterned after
        # IPython.core.magics.ScriptMagics.shebang.

        args = parse_argstring(self.powershell, line)

        with open(self._cell_file_name, mode='w') as f:
            f.write(cell)

        cmd = 'PowerShell -ExecutionPolicy RemoteSigned -File {}\r\n'
        cmd = cmd.format(self._cell_file_name)

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
