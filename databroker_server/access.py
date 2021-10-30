from enum import Enum
from typing import List


class AccessAction(Enum):
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    DELETE = "delete"


class AccessChecker():

    def is_allowed(user_id: str, data_session_id: str, action: AccessAction) -> bool:
        # user_id identifies a user uniquely in the system.
        # data_session_id identifies a group of runs and is stored in the start document
        # action enumerates possible actions that are being performed
        # The intention is that these three pieces can be used to get extra information.
        raise NotImplementedError()


class BnlChecker(AccessChecker):
    def __init__(self):
        super().__init__()

    def is_allowed(user_id: str, data_session_id: str, action: AccessAction) -> bool:
        if action == Action.RETRIEVE:
            return True
        else:
            return False
        
        # Should figure these permissions out later.
        return False
