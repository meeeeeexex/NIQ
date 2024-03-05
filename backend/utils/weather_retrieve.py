import calendar
from datetime import datetime
import requests

api_key = "1b90efcca5c18209dbdf7db569a4a72d"


def cast_city_country_from_code(city_code: str):
    city, country = city_code.split(',')
    country = country.strip()
    return city, country


def extract_last_month_data(date: datetime):
    if date.month != 1:
        return calendar.monthrange(date.year, date.month - 1)[1], date.year

    return calendar.monthrange(date.year - 1, 12)[1], date.year - 1


def get_month_data(city, today_temp):
    avg_temp: float
    monthly_data = []

    min_temp = today_temp
    max_temp = today_temp

    current_date = datetime.today()

    amount_of_days, last_month_year = extract_last_month_data(current_date)

    year = current_date.year if last_month_year == current_date.year else last_month_year
    month = current_date.month - 1 if last_month_year == current_date.year else 12

    for day in range(current_date.day, amount_of_days + 1):
        date = datetime(year, month, day)
        daily_temp = get_weather(city, date)

        monthly_data.append(daily_temp)
        min_temp = min(min_temp, daily_temp)
        max_temp = max(max_temp, daily_temp)

    for day in range(1, current_date.day + 1):
        date = datetime(current_date.year, current_date.month, day)
        daily_temp = get_weather(city, date)

        monthly_data.append(daily_temp)
        min_temp = min(min_temp, daily_temp)
        max_temp = max(max_temp, daily_temp)

    avg_temp = round(
        sum(monthly_data) / len(monthly_data), 1
    )
    return min_temp, max_temp, avg_temp


def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius)


def extract_lat_lot(city, country):
    params = {
        "q": f"{city},{country}",
        "appid": api_key
    }

    url = f"http://api.openweathermap.org/geo/1.0/direct"
    response = requests.get(url, params=params)
    response.raise_for_status()
    res = response.json()[0]
    return res['lat'], res['lon']


def get_weather(city_with_country_code, date: datetime):
    city, country = cast_city_country_from_code(city_with_country_code)
    lat, lon = extract_lat_lot(city, country)
    params = {
        "lat": lat,
        "lon": lon,
        "dt": int(date.timestamp()),
        "appid": api_key,
        "units": "metric"
    }
    url = f"http://api.openweathermap.org/data/3.0/onecall/timemachine"
    response = requests.get(url, params=params)
    response.raise_for_status()

    weather = response.json().get('data')[0]
    temperature = round(weather.get('temp'))
    return temperature
