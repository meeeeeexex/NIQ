from orm.models import Weather

from utils.weather_retrieve import cast_city_country_from_code


def create_weather_by_loc(db_session, location, weather, min_m, max_m, avg_m):
    db_weather = Weather(location=location, min_month=min_m, max_month=max_m,
                         weather=weather, avg_month=avg_m)
    db_session.add(db_weather)
    db_session.commit()
    db_session.refresh(db_weather)
    return db_weather


def get_cities(db_session):
    result = db_session.query(Weather).all()
    cities = []
    for row in result:
        name, country_code = cast_city_country_from_code(row.location)
        cities.append({'id': row.id, 'name': name, 'country_code': country_code})

    return cities
