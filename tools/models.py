import uuid

from sqlalchemy import Column, String, DATETIME
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.sql.functions import func

from tools.database_pg import Base


class City(Base):

    __tablename__ = 'city'

    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda : str(uuid.uuid4()))
    chinese_name = Column(String(255))
    ad_code = Column(String(255))
    city_code = Column(String(255))
    created_at = Column(DATETIME, server_default=func.now())
    def __repr__(self):
        return f"<City(id={self.id}, chinese_name='{self.chinese_name}', ad_code={self.ad_code}, city_code={self.city_code}, create_at={self.created_at})>"