import requests

def get_coordinates(city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200 and response.text.strip():
        try:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
        except ValueError as e:
            print("Ошибка разбора JSON:", e)
    print("Не удалось получить координаты города")
    return None, None

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    return response.json()

def get(city):
    lat, lon = get_coordinates(city)
    if lat and lon:
        weather = get_weather(lat, lon)
        current = weather.get("current_weather", {})
        temperature = current.get("temperature")
        windspeed = current.get("windspeed")
        st = ''
        st += f"Погода в городе {city}:\n"
        st += f"Температура: {temperature}°C\n"
        st += f"Скорость ветра: {windspeed} км/ч"
        
        return st
    else:
        return "Не удалось получить координаты города"
