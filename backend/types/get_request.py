from pydantic import BaseModel
from typing import Any, Mapping, Literal, Optional


FilterInfo = Mapping[str, Any]
SortInfo = Mapping[str, Literal['asc', 'desc']]


class PaginationInfo(BaseModel):
    page: int = 1
    page_size: int = 20
    offset: int = 0


class GetRequest(BaseModel):
    filter: Optional[FilterInfo] = None
    sort: Optional[SortInfo] = None
    pagination: PaginationInfo = PaginationInfo()
