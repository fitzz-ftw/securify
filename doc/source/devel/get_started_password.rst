Password Double Check
=====================

.. currentmodule:: securify.input.password

The :class:`PasswordDoubleCheck` class is a callable utility to ensure secure 
password entry with bot protection.

Basic Configuration
-------------------

You can configure the behavior via properties. Let's see how they work:



>>> from securify.input.password import PasswordDoubleCheck
>>> checker = PasswordDoubleCheck(min_delay=2.0)

>>> checker
PasswordDoubleCheck(min_delay: 2.00, require_terminal: True)

Testing the getters and setters

>>> checker.min_delay
2.0

>>> checker.min_delay = 1.0
>>> checker.min_delay
1.0

>>> checker.require_terminal = False
>>> checker.require_terminal
False

Customizing Prompts
-------------------

You can set default prompts that will be used during the call:


>>> checker.prompt1 = "New Password: "
>>> checker.prompt1
'New Password: '
>>> checker.prompt2 = "Confirm Password: "
>>> checker.prompt2
'Confirm Password: '

Validation State
----------------

The :attr:`PasswordDoubleCheck.is_valid` property tracks if the last attempt was successful.


>>> checker.is_valid
False

After a successful :meth:`PasswordDoubleCheck.__call__`, this would turn True.
We can manually reset it for a new attempt:

>>> checker.reset()
>>> checker.is_valid
False

.. rubric:: Technical Background: TTY Detection in Doctests

By default, PasswordDoubleCheck enforces a "Security First" policy: 
it refuses to run unless it detects a real interactive terminal (TTY). 
This mechanism ensures that the tool only processes input from a secure, 
interactive source.

If the input is piped from a script or another non-interactive process, 
the checker will reject the operation. This prevents the application 
from participating in insecure workflows where passwords might be handled 
through unsafe channels.

When running this doctest within an active terminal session, 
:external+python:meth:`sys.stdin.isatty() <io.IOBase.isatty>` naturally returns True. To demonstrate how the 
class rejects non-interactive usage and to show the resulting security error, 
we temporarily override the :external+python:meth:`sys.stdin.isatty() <io.IOBase.isatty>` method to return False. 
This allows you 
to see the :exc:`PasswordTerminalError`` in action and understand how the tool 
enforces interactive-only access.

>>> checker.require_terminal = True
>>> import sys
>>> old_isatty = sys.stdin.isatty
>>> sys.stdin.isatty = lambda: False

>>> checker("Test Password: ") #doctest: +NORMALIZE_WHITESPACE
Traceback (most recent call last): 
    ...
securify.input.exceptions.PasswordTerminalError: 
    Operation rejected: Input is not a terminal (TTY).

>>> sys.stdin.isatty = old_isatty

Simulating User Input
----------------------

The :class:`PasswordDoubleCheck` class is designed for interactive use. 
To demonstrate its behavior in a non-interactive environment like this 
documentation, we use a helper class called :class:`StubPassword`.

This stub acts as a "script" for our tests:

* **State Management:**
  It uses a Python generator to remember which password to return next.

* **Timing Simulation:** 
  It uses :external+python:func:`time.sleep` to simulate the time a human needs to 
  type. This allows us to test security features like the minimum delay.
* **Visibility:** 
  It prints the prompt strings so you can see exactly when the application 
  asks for input.

>>> import time

.. _stubpassword-label:

>>> class StubPassword:
...     def __init__(self):
...         self.generate = self._generate()
...     def _generate(self):
...         # first run 
...         yield "secret"
...         yield "secret"
...         # second run 
...         yield "secret"
...         time.sleep(2)
...         yield "secret"
...         # third run 
...         yield "secret"
...         time.sleep(2)
...         yield "sacrat"
...     def __call__(self, prompt):
...         print(prompt, flush=True)
...         return next(self.generate)

Initialize the stub passwordgenerator.

>>> stubgetpasswd = StubPassword()



>>> checkpw = PasswordDoubleCheck(min_delay=1.5, pwcall=stubgetpasswd)

Handling Fast Input
^^^^^^^^^^^^^^^^^^^^

To simulate fast input, the :ref:`first run <stubpassword-label>` part of the 
generator will be used. Since there is no delay between the first two yields, 
it will trigger a speed error.

>>> checkpw()
Traceback (most recent call last):
    ...
securify.input.exceptions.PasswordSpeedError: Input rejected: Entry was too fast (0.00s). Minimum required: 1.5s.

Tracking the Validation State
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :attr:`~PasswordDoubleCheck.is_valid` property allows you to check whether 
the last password entry was successful without having to handle exceptions 
immediately.

After a failed attempt (like the speed error above), the state remains invalid:

>>> checkpw.is_valid
False

When we trigger the next attempt, the :ref:`second run <stubpassword-label>` of 
our stub is used. This time, the :external+python:func:`time.sleep(2)<time.sleep>` ensures that the 
security requirements are met:

>>> checkpw()
Enter password: 
Retype password: 
'secret'

Now that the verification was successful, the state changes:

>>> checkpw.is_valid
True

.. rubric:: Resetting the Checker

If you want to reuse the same checker instance for a completely 
new process, you can use the :meth:`~PasswordDoubleCheck.reset()` method. 
This clears the internal validation state:

>>> checkpw.reset()

Handling Mismatched Passwords
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The final scenario demonstrates what happens when the two entered passwords 
do not match. This uses the :ref:`third run <stubpassword-label>` of our stub, 
where we intentionally provided "secret" and "sacrat".

Even though the typing delay requirement was met, the library identifies 
the mismatch and raises a specific exception:

>>> checkpw()
Traceback (most recent call last):
    ...
securify.input.exceptions.PasswordMismatchError: Verification failed: Passwords do not match.

As expected, the validation state remains `False` because the security 
check was not completed successfully:

>>> checkpw.is_valid
False
