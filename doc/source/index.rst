Securify
========

**Securify** is a lightweight Python library designed to handle sensitive user input with an extra layer of security. It focuses on secure password entry, terminal validation, and timing-based protection against automated scripts.

Key Features
------------

* **Secure Input:** Wraps standard library tools to ensure passwords are not echoed to the terminal.
* **Terminal Validation:** Ensures that sensitive inputs only occur in interactive TTY environments.
* **Timing Protection:** Prevents automated "brute-force" or rapid-fire scripted inputs by enforcing a minimum typing delay.
* **Double-Check Logic:** Built-in verification flow to reduce user typos.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   index_get_started

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation:

   devel/securify_module

.. toctree::
   :maxdepth: 1
   :caption: Project Information:

   about
   changelog_link
   license_lgpl21
   genindex
   modindex



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
