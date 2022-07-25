Installing XOA Test Config Converter
=====================================

XOA Test Config Converter is available to install and upgrade via the `Python Package Index <https://pypi.org/>`_. Alternatively, you can also install and upgrade from the source file.

* If you prefer installing/upgrading/uninstalling automatically, go to Section `From PyPi Using pip`_.
* If you prefer installing/upgrading manually, go to Section `Manually From Source`_.

Prerequisites
-------------

Before installing XOA Test Config Converter, please make sure your environment has installed `Python <https://www.python.org/>`_ and ``pip``.

Python
^^^^^^^

XOA Test Config Converter requires that you `install Python <https://realpython.com/installing-python/>`_  on your system.

.. note:: 

    XOA Test Config Converter requires Python >= 3.8.

``pip``
^^^^^^^

Make sure ``pip`` is installed on your system. ``pip`` is the `package installer for Python <https://packaging.python.org/guides/tool-recommendations/>`_ . You can use it to install packages from the `Python Package Index <https://pypi.org/>`_  and other indexes.

Usually, ``pip`` is automatically installed if you are:

* working in a `virtual Python environment <https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments>`_ (`virtualenv <https://virtualenv.pypa.io/en/latest/#>`_ or `venv <https://docs.python.org/3/library/venv.html>`_ ). It is not necessary to use ``sudo pip`` inside a virtual Python environment.
* using Python downloaded from `python.org <https://www.python.org/>`_ 

If you don't have ``pip`` installed, you can:

* Download the script, from https://bootstrap.pypa.io/get-pip.py.
* Open a terminal/command prompt, ``cd`` to the folder containing the ``get-pip.py`` file and run:

.. tab:: Windows

    .. code-block:: doscon
        :caption: Install pip in Windows environment.

        > py get-pip.py

.. tab:: macOS/Linux

    .. code-block:: console
        :caption: Install pip in macOS/Linux environment.

        $ python3 get-pip.py

.. seealso::

    Read more details about this script in `pypa/get-pip <https://github.com/pypa/get-pip>`_.

    Read more about installation of ``pip`` in `pip installation <https://pip.pypa.io/en/stable/installation/>`_.


From PyPi Using ``pip``
------------------------

Install
^^^^^^^^

``pip`` is the recommended installer for XOA Test Config Converter. The most common usage of ``pip`` is to install from the `Python Package Index <https://pypi.org/>`_ using `Requirement Specifiers <https://pip.pypa.io/en/stable/cli/pip_install/#requirement-specifiers>`_.

.. tab:: Windows
    :new-set:

    .. code-block:: doscon
        :caption: Install XOA Test Config Converter in Windows environment from PyPi.

        > pip install xoa-converter         # latest version
        > pip install xoa-converter==1.0.1     # specific version
        > pip install xoa-converter>=1.0.1     # minimum version

.. tab:: macOS/Linux

    .. code-block:: console
        :caption: Install XOA Test Config Converter in macOS/Linux environment from PyPi.

        $ pip install xoa-converter         # latest version
        $ pip install xoa-converter==1.0.1     # specific version
        $ pip install xoa-converter>=1.0.1     # minimum version

Upgrade
^^^^^^^^

To upgrade XOA Test Config Converter package from PyPI:

.. tab:: Windows
    :new-set:
    
    .. code-block:: doscon
        :caption: Upgrade XOA Test Config Converter in Windows environment from PyPi.

        > pip install xoa-converter --upgrade

.. tab:: macOS/Linux

    .. code-block:: console
        :caption: Upgrade XOA Test Config Converter in macOS/Linux environment from PyPi.

        $ pip install xoa-converter --upgrade


Uninstall
^^^^^^^^^^^

To uninstall XOA Test Config Converter using ``pip``:

.. tab:: Windows
    :new-set:

    .. code-block:: doscon
        :caption: Uninstall XOA Test Config Converter in Windows environment.

        > pip uninstall xoa-converter

.. tab:: macOS/Linux

    .. code-block:: console
        :caption: Uninstall XOA Test Config Converter in macOS/Linux environment.

        $ pip uninstall xoa-converter

.. seealso::

    For more information, see the `pip uninstall <https://pip.pypa.io/en/stable/cli/pip_uninstall/#pip-uninstall>`_ reference.



Manually From Source
----------------------

Install or Upgrade
^^^^^^^^^^^^^^^^^^^

If for some reason you need to install or upgrade XOA Test Config Converter manually from source, the steps are:

First, make sure Python packages `wheel <https://wheel.readthedocs.io/en/stable/>`_ and  `setuptools <https://setuptools.pypa.io/en/latest/index.html>`_ are installed on your system. Install ``wheel`` and ``setuptools`` using ``pip``:

.. tab:: Windows
    :new-set:

    .. code-block:: doscon
        :caption: Install ``wheel`` and ``setuptools`` in Windows environment.

        > pip install wheel setuptools

.. tab:: macOS/Linux

    .. code-block:: console
        :caption: Install ``wheel`` and ``setuptools`` in macOS/Linux environment.

        $ pip install wheel setuptools

Then, download the XOA Test Config Converter source distribution from `XOA Test Config Converter Releases <https://github.com/xenanetworks/open-automation-python-api/releases>`_. Unzip the archive and run the ``setup.py`` script to install the package:

.. tab:: Windows
    :new-set:

    .. code-block:: doscon
        :caption: Install XOA Test Config Converter in Windows environment from source.

        > python setup.py install

.. tab:: macOS/Linux

    .. code-block:: console
        :caption: Install XOA Test Config Converter in macOS/Linux environment from source.

        $ python3 setup.py install


If you want to distribute, you can build ``.whl`` file for distribution from the source:

.. tab:: Windows
    :new-set:

    .. code-block:: doscon
        :caption: Build XOA Test Config Converter wheel in Windows environment for distribution.

        > python setup.py bdist_wheel

.. tab:: macOS/Linux

    .. code-block:: console
        :caption: Build XOA Test Config Converter wheel in macOS/Linux environment for distribution.

        $ python3 setup.py bdist_wheel
