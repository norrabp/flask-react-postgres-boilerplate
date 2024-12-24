from typing import Optional
from backend.types.get_request import PaginationInfo

MAX_PAGE_SIZE = 100


def get_pagination(pagination: Optional[PaginationInfo]) -> PaginationInfo:
    if pagination is None:
        pagination = PaginationInfo()
    if pagination.page_size > MAX_PAGE_SIZE:
        pagination.page_size = MAX_PAGE_SIZE
    return pagination
