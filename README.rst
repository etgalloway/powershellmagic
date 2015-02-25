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
       ...: get-process ipython, python
       ...:

    Handles  NPM(K)    PM(K)      WS(K) VM(M)   CPU(s)     Id ProcessName
    -------  ------    -----      ----- -----   ------     -- -----------
         22       2      808       1816     7     0.00   3604 ipython
        162      16    25752      30280   109     1.37   5320 python
