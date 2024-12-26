import enum
from typing import Optional, TypeVar, Union

from typing_extensions import TypeAlias, TypeGuard

_T = TypeVar('_T')

class _NotModifiedType(enum.Enum):
    token = enum.auto()

NOT_MODIFIED: _NotModifiedType = _NotModifiedType.token
Modification: TypeAlias = Union[_T, _NotModifiedType]


def get_modification(obj: Modification[_T], default: _T) -> _T:
    if is_modified(obj):
        return obj
    return default

def is_modified(obj: Modification[_T], previous: Optional[_T] = None) -> TypeGuard[_T]:
    if obj is not NOT_MODIFIED:
        if obj != previous:
            return True
    return False
