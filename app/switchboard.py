from __future__ import annotations

from dataclasses import dataclass

from app.users import User, ForeignUser, LocalUser


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_count = 0
        self._phones_in_use: set[str] = set()

    @staticmethod
    def create_user(u_id: int, u_name: str, u_phone: str) -> User:
        if u_phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(u_id, u_name, u_phone)
        return ForeignUser(u_id, u_name, u_phone)

    def _validate_format(self, c_id: str, c_name: str, c_phone: str, r_id: str, r_name: str, r_phone: str, raw_call: str) -> None:
        if not (c_id.isnumeric() and int(c_id) >= 0) or not (r_id.isnumeric() and int(r_id) >= 0):
            raise AttributeError(f"Input string must contain 2 positive int id, actual: {raw_call}")

        if len(c_name) == 0 or len(r_name) == 0:
            raise AttributeError(f"Input string must contain non-empty names, actual: {raw_call}")
        
        if not c_name.replace(" ", "").isalpha() or not r_name.replace(" ", "").isalpha():
            raise AttributeError(f"Input string must contain alphabetical caller and receiver name, actual: {raw_call}")

        if len(c_phone) < 11 or len(c_phone) > 16 or not c_phone.startswith("+") or not c_phone[1::].isnumeric():
            raise AttributeError(f"Input string must contain valid caller phone number, actual: {c_phone}")
        
        if len(r_phone) < 11 or len(r_phone) > 16 or not r_phone.startswith("+") or not r_phone[1::].isnumeric():
            raise AttributeError(f"Input string must contain valid receiver phone number, actual: {r_phone}")

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        segments = [segment.strip() for segment in raw_call.split(",")]
        if len(segments) != 6:
            raise AttributeError(f"Input string must contain 6 values separated by ',', actual: {raw_call}")
        
        c_id, c_name, c_phone, r_id, r_name, r_phone = segments
        self._validate_format(c_id, c_name, c_phone, r_id, r_name, r_phone, raw_call)

        if c_phone == r_phone:
            raise AttributeError("Caller and receiver cannot have same phone")

        if c_phone in self._phones_in_use:
            raise AttributeError("Caller phone already in call")
        if r_phone in self._phones_in_use:
            raise AttributeError("Receiver phone already in call")

        caller = self.create_user(int(c_id), c_name, c_phone)
        receiver = self.create_user(int(r_id), r_name, r_phone)

        self._phones_in_use.add(c_phone)
        self._phones_in_use.add(r_phone)

        newCall = ActiveCall(caller, receiver)
        if newCall.is_cross_border:
            self._cross_border_count += 1

        self._active_calls.append(newCall)
        return newCall

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_count
