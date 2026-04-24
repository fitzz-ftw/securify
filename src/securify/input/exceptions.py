# File: src/securify/exceptions.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
exceptions
===============================

This module contains specific exception classes for password handling.
"""

from pathlib import Path

from securify.base.exceptions import SecurifyError


class PasswordError(SecurifyError):
    """
    Base exception for all password-related errors in securify.

    Catch Order: 
        * PasswordError 
        * SecurifyError 
        * Exception
    """
    pass

class PasswordMismatchError(PasswordError):
    """
    Raised when the two password entries do not match.

    Catch Order: 
        * PasswordMismatchError 
        * PasswordError 
        * SecurifyError 
        * Exception
    """
    pass

class PasswordSpeedError(PasswordError):
    """
    Raised when password entry is faster than the allowed threshold.

    Catch Order: 
        * PasswordSpeedError 
        * PasswordError 
        * SecurifyError 
        * Exception
    """
    pass

class PasswordTerminalError(PasswordError):
    """
    Raised when a terminal is required but not available.

    Catch Order: 
        * PasswordTerminalError
        * PasswordError
        * SecurifyError
        * Exception
    """
    pass

if __name__ == "__main__": # pragma: no cover
    from doctest import FAIL_FAST, testfile
    
    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_exceptions.rst"
    
    if test_file.exists():
        print(f"--- Running Doctest for {test_file.name} ---")
        doctestresult = testfile(
            str(test_file),
            module_relative=False,
            verbose=be_verbose,
            optionflags=option_flags,
        )
        test_failed += doctestresult.failed
        test_sum += doctestresult.attempted
        if test_failed == 0:
            print(f"\nDocTests passed without errors, {test_sum} tests.")
        else:
            print(f"\nDocTests failed: {test_failed} tests.")
    else:
        print(f"⚠️ Warning: Test file {test_file.name} not found.")
