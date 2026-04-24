# File: src/securify/input/password.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
password
===============================

This module provides tools for secure password input verification.
"""

import sys
import time
from getpass import getpass
from pathlib import Path
from typing import Any, Callable

from securify.input.exceptions import (
    PasswordMismatchError,
    PasswordSpeedError,
    PasswordTerminalError,
)


class PasswordDoubleCheck:
    """
    A class to verify a password by requiring two consecutive entries.
    
    This class is callable and checks for a minimum time delay between 
    inputs and ensures the input is coming from a terminal.
    """

    def __init__(
        self,
        *,
        min_delay: float = 1.5,
        require_terminal: bool = True,
        prompt1: str = "",
        prompt2: str = "",
        **kwargs: Any,
    ):
        """
        Initialize the checker with prompts and security constraints.

        :param min_delay: Minimum time in seconds between entries to prevent bots.
        :param require_terminal: If True, ensures the input source is a TTY.
        :param prompt1: The message shown for the first password entry.
        :param prompt2: The message shown for the second password entry.
        :param kwargs: Additional arguments, supports 'pwcall' for input function.
        """
        self._min_delay = min_delay
        self._require_terminal = require_terminal
        self._prompt1 = prompt1
        self._prompt2 = prompt2
        self._valid:bool = False
        self._pw_input_func: Callable[[str], str] = kwargs.get("pwcall", getpass)

    @property
    def prompt1(self) -> str:
        """
        The message shown for the first password entry **(rw)**.

        :param value: The new prompt string for the first entry.
        :returns: The current prompt string for the first entry.
        """
        return self._prompt1
    
    @prompt1.setter
    def prompt1(self, value:str) -> None:
        """
        The message shown for the first password entry **(rw)**.

        :param value: The new prompt string for the first entry.
        :returns: The current prompt string for the first entry.
        """
        self._prompt1= value

    @property
    def prompt2(self) -> str:
        """
        The message shown for the second password entry **(rw)**.

        :param value: The new prompt string for the second entry.
        :returns: The current prompt string for the second entry.
        """
        return self._prompt2

    @prompt2.setter
    def prompt2(self, value: str) -> None:
        """
        The message shown for the second password entry **(rw)**.

        :param value: The new prompt string for the second entry.
        :returns: The current prompt string for the second entry.
        """
        self._prompt2 = value

    @property
    def min_delay(self) -> float:
        """
        Minimum time in seconds between entries to prevent bots **(rw)**.

        :param value: The delay duration in seconds.
        :returns: The current minimum delay in seconds.
        """
        return self._min_delay
    
    @min_delay.setter
    def min_delay(self, value:float)-> None:
        """
        Minimum time in seconds between entries to prevent bots **(rw)**.

        :param value: The delay duration in seconds.
        :returns: The current minimum delay in seconds.
        """
        self._min_delay = value

    @property
    def require_terminal(self)->bool:
        """
        Requirement for a real interactive terminal (TTY) **(rw)**.

        :param value: Set to True to enforce TTY check.
        :returns: True if a TTY is required for input.
        """
        return self._require_terminal
    
    @require_terminal.setter
    def require_terminal(self, value:bool) -> None:
        """
        Requirement for a real interactive terminal (TTY) **(rw)**.

        :param value: Set to True to enforce TTY check.
        :returns: True if a TTY is required for input.
        """
        self._require_terminal = value

    @property
    def is_valid(self)->bool:
        """
        The success status of the last verification attempt **(ro)**.

        :returns: True if the passwords matched and all constraints were met.
        """
        return self._valid
    
    def reset(self) -> None:
        """
        Reset the internal validation status to False.
        """
        self._valid = False

    def __call__(self, prompt1: str = "", 
                 prompt2: str = "") -> str:
        """
        Execute the double-entry verification process.

        :param prompt1: Optional override for the first prompt.
        :param prompt2: Optional override for the second prompt.
        :raises PasswordTerminalError: If require_terminal is True but no TTY is detected.
        :raises PasswordMismatchError: If the two entered passwords do not match.
        :raises PasswordSpeedError: If the entry was faster than min_delay.
        :returns: The verified password string.
        """
        self._valid = False
        prompt1 = prompt1 or self._prompt1 or "Enter password: "

        prompt2 = prompt2 or self._prompt2 or "Retype password: "

        # 1. Terminal check
        if self._require_terminal and not sys.stdin.isatty():
            raise PasswordTerminalError("Operation rejected: Input is not a terminal (TTY).")

        # 2. First password entry
        first_input = self._pw_input_func(prompt1)
        
        # Start timer immediately after the first 'Enter'
        start_time = time.perf_counter()

        # 3. Second password entry
        second_input = self._pw_input_func(prompt2)
        
        # End timer after the second 'Enter'
        end_time = time.perf_counter()

        # 4. Validation: Matching
        if first_input != second_input:
            raise PasswordMismatchError("Verification failed: Passwords do not match.")

        # 5. Validation: Speed (Bot-Protection)
        duration = end_time - start_time
        if duration < self._min_delay:
            raise PasswordSpeedError(
                f"Input rejected: Entry was too fast ({duration:.2f}s). "
                f"Minimum required: {self._min_delay}s."
            )

        self._valid=True
        return first_input
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(min_delay: {self._min_delay:.2f}, "
                f"require_terminal: {self._require_terminal})")

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
    test_file = testfiles_dir / "get_started_password.rst"
    
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
