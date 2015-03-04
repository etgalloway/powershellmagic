===============
powershellmagic
===============

`powershellmagic` is an IPython extension, modeled after IPython's 
`%%script <http://ipython.org/ipython-doc/dev/interactive/magics.html#cellmagic-script>`_  
magic, that supports the execution of IPython cells written in 
Windows PowerShell.

Install
=======

As a Python package:

.. code::

    $ pip install powershellmagic

As an IPython extension:

.. code::

    In [1]: %install_ext https://raw.github.com/etgalloway/powershellmagic/master/powershellmagic.py

Use
===

.. code::

    In [1]: %load_ext powershellmagic

    In [2]: %%powershell
       ...: Get-WMiObject -Class Win32_Process |
       ...:     Where-Object { $_.Name -like "*python.exe" } |
       ...:     Select-Object ProcessName, ProcessID, ParentProcessId |
       ...:     Format-Table -AutoSize
       ...:

    ProcessName ProcessID ParentProcessId
    ----------- --------- ---------------
    ipython.exe      5600            5616
    python.exe       1740            5600
