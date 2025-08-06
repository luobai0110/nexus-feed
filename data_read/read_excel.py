# data_read/read_excel.py
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from tools.city_dao import CityDao
from tools.database_pg import get_db_session
from tools.models import City


def read_city():
    cities = []
    df = pd.read_excel('../temp-data/AMap_adcode_citycode.xlsx')
    # 修正过滤条件：处理 NaN 值
    filtered_df = df[df['citycode'].notna() & (df['citycode'] != '\\N')]

    for _, rows in filtered_df.iterrows():
        city = City(
            chinese_name=str(rows['中文名']),
            city_code=str(rows['citycode']) if pd.notna(rows['citycode']) else None,
            ad_code=str(rows['adcode']) if pd.notna(rows['adcode']) else None,
        )
        cities.append(city)
    return cities


if __name__ == '__main__':
    # 获取数据库会话
    db_session = get_db_session()

    try:
        dao = CityDao(db_session)
        cities = read_city()
        print(f"准备保存 {len(cities)} 个城市")

        saved_cities = dao.save_cities(cities)
        if saved_cities:
            print(f"成功保存 {len(saved_cities)} 个城市")
        else:
            print("保存城市失败")

    except Exception as e:
        print(f"程序执行失败: {e}")
    finally:
        # 确保关闭数据库连接
        db_session.close()