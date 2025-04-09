import datetime
from datetime import datetime

import requests
import geocoder


API_KEY = "a2f1e1675826c6cbfccb782ef1f24536"
HOST = "https://api.openweathermap.org/data/2.5/"
WEEK_DAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]


def get_weather():
    g = geocoder.ip("me")
    lat, lng = g.lat, g.lng

    res = requests.get(f"{HOST}forecast?lat={lat}&lon={lng}&appid={API_KEY}&units=metric&lang=ru").json()
    return [
        extract_data(point) for point in res["list"]
    ]


def extract_data(one_point):
    match one_point:
        case {
            "weather": [{"description": description}],
            "dt_txt": txt_date,
            "main": {"temp": temp, "pressure": pressure},
            "wind": {"deg": deg, "speed": speed}
        }:
            return {
                "description": description,
                "time": datetime.strptime(txt_date, "%Y-%m-%d %H:%M:%S"),
                "temp": round(temp),
                "pressure": round(pressure / 1000 * 750),
                "wind_deg": deg,
                "wind_speed": round(speed, 1)
            }


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_weather())
