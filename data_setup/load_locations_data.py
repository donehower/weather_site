import json
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.engine.url import URL


def main():
    db_url = {'drivername': 'postgres',
              'username': 'sarahd',
              'password': 'avocado_good',
              'host': 'localhost',
              'port': 5432,
              'database': 'weather_site'}

    engine = create_engine(URL(**db_url))

    meta = MetaData(engine)
    locations = Table('locations', meta,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('name', String(255), unique=True, primary_key=True),
                      Column('city', String(255)),
                      Column('state_short', String(255)),
                      Column('state_full', String(255)),
                      Column('station_id', String(10), unique=True),
                      Column('coord', Text),
                      Column('forecast_url', String(255)),
                      Column('hourForecast_url', String(255)))
    ins = inspect(engine)
    if locations in ins.get_table_names():
        locations.drop()
    meta.create_all(bind=engine)

    with open('locations_details_v2.txt', encoding='utf-8') as f:
        data = json.loads(f.read())

    conn = engine.connect()
    conn.execute(locations.insert(), data)
    conn.close()


if __name__ == '__main__':
    main()
