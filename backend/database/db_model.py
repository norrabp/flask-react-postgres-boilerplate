from sqlalchemy.dialects.postgresql import UUID
from backend.extensions.extensions import db
from backend.util.pagination import get_pagination
from typing import List, Optional
from backend.types.get_request import FilterInfo, SortInfo, PaginationInfo
from datetime import datetime
import uuid


class Model(db.Model):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def delete(self, hard_delete: bool = False):
        if hard_delete:
            db.session.delete(self)
        else:
            self.deleted_at = datetime.now()
        db.session.commit()

    def create(self, commit: bool = True):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
    
    def update(self, commit: bool = True):
        self.updated_at = datetime.now()
        if commit:
            db.session.commit()
        return self
    
    @classmethod
    def get_list(
        cls,
        filter: Optional[FilterInfo] = None,
        sort: Optional[SortInfo] = None,
        pagination: Optional[PaginationInfo] = None,
        with_deleted: bool = False
    ) -> tuple[List['Model'], bool]:
        query, has_next_page = cls.get_list_query_obj(filter, sort, pagination, with_deleted)
        return query.all(), has_next_page

    
    @classmethod
    def get_list_query_obj(
        cls,
        filter: Optional[FilterInfo] = None,
        sort: Optional[SortInfo] = None,
        pagination: Optional[PaginationInfo] = None,
        with_deleted: bool = False
    ) -> tuple[List['Model'], bool]:
        query = cls.query
        pagination = get_pagination(pagination)
        if not with_deleted:
            query = query.filter_by(deleted_at=None)
        if filter:
            query = query.filter_by(**filter)
        if sort:
            for column, direction in sort.items():
                column_attr = getattr(cls, column)
                query = query.order_by(
                    column_attr.desc() if direction == 'desc' else column_attr.asc()
                )

        total_count = query.count()
        query = query.limit(pagination.page_size).offset(
            (pagination.page - 1) * pagination.page_size + pagination.offset
        )

        return query, total_count > (
            pagination.page_size * pagination.page + pagination.offset
        )
    
    def get_or_create(self, filter: Optional[FilterInfo] = None, commit: bool = True):
        query = self.query.filter_by(**filter).first()
        if not query:
            self.create(commit)
        return query
    
    def update_or_create(self, filter: Optional[FilterInfo] = None, commit: bool = True):
        query = self.query.filter_by(**filter).first()
        if not query:
            self.create(commit)
        else:
            self.update(commit)
        return query
    
