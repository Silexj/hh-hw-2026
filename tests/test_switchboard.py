import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1

def test_register_call_not_counts_cross_border() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )

    assert switchboard.get_cross_border_calls_count() == 0

def test_register_call_raise_error_with_incorrect_arguments() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError, 
                       match="Input string must contain 6 values separated by ',', actual: *"):
        switchboard.register_call(
            "1,Ivan Ivanov,+79990000000,2,Petr Petrov+78880000000"
        )

def test_register_call_has_no_active_at_init() -> None:
    switchboard = Switchboard()

    assert switchboard.get_active_calls_count() == 0
    assert switchboard.get_cross_border_calls_count() == 0

def test_register_call_raise_error_with_incorrect_id() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError, 
                       match="Input string must contain 2 positive int id, actual: *"):
        switchboard.register_call(
            "1asd,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
        )

def test_register_call_raise_error_with_negative_id() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError, 
                       match="Input string must contain 2 positive int id, actual: *"):
        switchboard.register_call(
            "-1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
        )

def test_register_call_raise_error_with_empty_name() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError, 
                       match="Input string must contain non-empty names, actual: *"):
        switchboard.register_call(
            "1,Ivan Ivanov,+79990000000,2,,+78880000000"
        )

def test_register_call_raise_error_with_no_country_code() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError, 
                       match="Input string must contain valid caller phone number, actual: *"):
        switchboard.register_call(
            "1,Ivan Ivanov,999990000000,2,Petr Petrov,+78880000000"
        )
    
def test_register_call_raise_error_with_empty_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError, 
                       match="Input string must contain valid caller phone number, actual: *"):
        switchboard.register_call(
            "1,Ivan Ivanov,,2,Petr Petrov,+78880000000"
        )

def test_register_call_with_spaces() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1  ,Ivan Ivanov  ,  +79990000000 ,  2, Petr Petrov,  +78880000000"
    )

def test_register_call_with_str_in_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError,
                       match="Input string must contain valid receiver phone number, actual: *"):
        switchboard.register_call(
            "1,Ivan Ivanov,+7429903528,2,Petr Petrov,+785af0000000"
        )

def test_register_call_with_small_len_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError,
                       match="Input string must contain valid receiver phone number, actual: *"):
        switchboard.register_call(
            "1,Ivan Ivanov,+7429903528,2,Petr Petrov,+785000"
        )

def test_register_call_with_big_len_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError,
                       match="Input string must contain valid receiver phone number, actual: *"):
        switchboard.register_call(
            "1,Ivan Ivanov,+7429903528,2,Petr Petrov,+78501231244525200"
        )

def test_register_call_with_same_receiver_phone_and_caller_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError,
                       match="Caller and receiver cannot have same phone"):
        switchboard.register_call(
            "1,Ivan Ivanov,+7429903528,2,Petr Petrov,+7429903528"
        )

def test_register_call_with_duplicate_phone() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    with pytest.raises(AttributeError,
                       match="Caller phone already in call"):
        switchboard.register_call(
            "1,Ivan Ivanov,+79990000000,4,Petr Petrov,+75551234567"
        )
    assert switchboard.get_active_calls_count() == 1

def test_register_call_with_invalid_name() -> None:
    switchboard = Switchboard()

    with pytest.raises(AttributeError,
                       match="Input string must contain alphabetical caller and receiver name, actual: *"):
        switchboard.register_call(
            "1,Ivan Iv#$anov,+79990000000,2,John Smith,+15551234567"
        )