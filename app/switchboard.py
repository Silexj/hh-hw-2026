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

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        strs = raw_call.split(",")
        
        if len(strs) != 6:
            raise AttributeError(f"Input string must contain 6 values separated by ',', actual: {raw_call}")
        
        c_id, c_name, c_phone, r_id, r_name, r_phone = strs;
        if not (c_id.isnumeric() and int(c_id) >= 0) or not (r_id.isnumeric() and int(r_id) >= 0):
            raise AttributeError(f"Input string must contain 2 positive int id, actual: {raw_call}")

        if len(c_name) == 0 or len(r_name) == 0:
            raise AttributeError(f"Input string must contain non-empty names, actual: {raw_call}")
        if (len(c_phone) == 0 or not c_phone.startswith("+")) \
            and (len(r_phone) or not c_phone.startswith("+")):
                raise AttributeError(f"Input string must contain valid phone number, actual: {raw_call}")

            
        caller = LocalUser(int(c_id), c_name, c_phone) if c_phone.startswith(LOCAL_PHONE_PREFIX) else ForeignUser(int(c_id), c_name, c_phone)
        receiver = LocalUser(int(r_id), r_name, r_phone) if r_phone.startswith(LOCAL_PHONE_PREFIX) else ForeignUser(int(r_id), r_name, r_phone)
        
        newCall = ActiveCall(caller, receiver)
        if newCall.is_cross_border:
            self._cross_border_count += 1

        self._active_calls.append(newCall)
        return newCall

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_count
