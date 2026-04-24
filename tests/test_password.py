import pytest

from securify.input.password import PasswordDoubleCheck, PasswordMismatchError, PasswordSpeedError


def test_successful_verification():
    """Test standard success case."""
    # Wir simulieren zwei identische Eingaben
    inputs = iter(["my_secure_pw", "my_secure_pw"])
    fake_getpass = lambda _: next(inputs)  # noqa: E731

    checker = PasswordDoubleCheck(
        min_delay=0.0,  # Keine Verzögerung im Test nötig
        require_terminal=False,
        pwcall=fake_getpass,
    )

    result = checker()

    assert result == "my_secure_pw"
    assert checker.is_valid is True


def test_password_mismatch():
    """Test if mismatch raises the correct custom exception."""
    inputs = iter(["pw1", "pw2"])
    fake_getpass = lambda _: next(inputs)  # noqa: E731

    checker = PasswordDoubleCheck(require_terminal=False, pwcall=fake_getpass)

    with pytest.raises(PasswordMismatchError):
        checker()

    assert checker.is_valid is False


def test_too_fast_input():
    """Test the bot-protection timing logic."""
    # Zwei schnelle Eingaben
    fake_getpass = lambda _: "constant_pw"  # noqa: E731

    # Wir setzen eine künstlich hohe Mindestdauer
    checker = PasswordDoubleCheck(min_delay=0.5, require_terminal=False, pwcall=fake_getpass)

    with pytest.raises(PasswordSpeedError) as excinfo:
        checker()

    # Prüfen, ob die Fehlermeldung die Zeit enthält
    assert "too fast" in str(excinfo.value)
    assert checker.is_valid is False


def test_reset_functionality():
    """Verify that reset sets is_valid back to False."""
    inputs = iter(["pw", "pw"])
    checker = PasswordDoubleCheck(
        min_delay=0, require_terminal=False, pwcall=lambda _: next(inputs)
    )

    checker()
    assert checker.is_valid is True

    checker.reset()
    assert checker.is_valid is False
