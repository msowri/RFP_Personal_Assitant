from sqlalchemy import Column,Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declared_attr
from typing import Any

class DomainObject:
    """common field."""
    id       = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String, nullable=False, default="admin")
    updated_by = Column(String, nullable=False, default="admin")
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    pagename = Column(String, nullable=True) #added for testing to verify the Dabase_URL Changes, in not required in future will remove.

    @declared_attr
    def __tablename__(cls) -> Any:
        # Use double underscores: __name__
        return type(cls).__name__.lower() + "s"