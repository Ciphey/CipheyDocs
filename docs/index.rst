.. Ciphey documentation master file, created by
   sphinx-quickstart on Thu Jun  4 18:32:21 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ciphey - Automated Decryption Tool
==================================

Ciphey is an automated decryption tool. Input text, get the decrypted text back.

        "But what type of encryption?"

That's the point. You don't know. 
Ciphey will figure it out for you.

Ciphey uses a deep neural network with a simple filtration system to approximate what something is encrypted with. And then a custom-built, customisable natural languge processing Language Checker Interface, which can detect when the given text becomes plaintext.

Usage
-----
To use as a console application:
.. code-block:: console

        ciphey [OPTIONS]

.. option:: -t <encrypted text>, --text <encrypted text>

        The encrypted text you want to decrypt.

.. option:: - "text"
        Ciphey can be ran with Ciphey [OPTIONS] - "text" too

.. option:: -- file.txt
        Open a file in Ciphey. Ciphey [OPTIONS] -- file.txt

.. option:: -q, --quiet

        Don't print out extra information such as the probability table. Useful for grepping the answer.

.. option:: -i, --info

        Use this option to get mroe information on the cipher used.

.. option:: -v, --verbose

        Turn on debug mode, which prints out the logs of the file.
        -v is debug mode.
        -vvv is trace mode.

.. option:: -w, --wordlist
        Use the given wordlist.

.. option:: -p, --param
        Pass a paramater to the language checker

.. option:: -l, --list-params
        List the params of the given module

.. option:: -c, --config
        Use the given config file.

.. option:: -C, --checker
        Use the given checker (such as regex)


Regex
------
To run Ciphey with Regex support, execute this:

.. code-block:: console
        ciphey -t = "text" -C regex -p regex.regex={

This says "-C regex" use the given checker Regex, "-p regex.regex={" pass the paraemter "regex.regex" with the value "{" to the regex checker. The value "{" is the regex we want to check against. Many CTF flags use {}.

Alternatively, if you have a large list of regex, check out the settings file which can store a regex list and be automatically used.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
        Installation Guide <install.rst>
        Extending Ciphey <extending.rst>
        References <reference.rst>
        What encryptions are implemented? <ciphers.rst>
        Configuration File <config.rst>
        Features <features.rst>
        How does it work? <howWork.rst>
        Settings File <settings.rst>
        Adding your own ciphers <makingCiphers.rst>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
