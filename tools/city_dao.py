import logging
from typing import TypeVar, Optional, List, Any

from sqlalchemy.orm import Session

from tools.models import City

T = TypeVar('T')


class BaseDao:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__)

    def _handle_exception(self, db_error: Exception, message: str) -> T:
        self.db.rollback()
        self.logger.error(f"{message}操作失败: {str(db_error)}")
        raise db_error

class CityDao(BaseDao):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_city(self, city_name: str) -> list[type[City]] | T:
        """根据城市名称获取城市"""
        try:
            return self.db.query(City).filter(City.chinese_name == city_name).all()
        except Exception as e:
            self.logger.error("获取城市失败", e)
            return self._handle_exception(e, "获取城市失败")
    def save_city(self, city: City) -> City | None:
        """保存城市"""
        try:
            self.db.add(city)
            self.db.commit()
            self.db.refresh(city)
            return city
        except Exception as e:
            self.logger.error("保存城市失败", e)

    def save_cities(self, cities: List[City]) -> List[City] | None:
        """保存城市"""
        try:
            self.db.add_all(cities)
            self.db.commit()
            for city in cities:
                self.db.refresh(city)
            return cities
        except Exception as e:
            self.logger.error("保存城市失败", e)