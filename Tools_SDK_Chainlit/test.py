import requests

location:str = "jjj"
OPENWEATHER_API_KEY = "f9ac4d4bae604c769ba184022252904"
response = requests.get(
    f"http://api.weatherapi.com/v1/current.json?key={OPENWEATHER_API_KEY}&q={location}"
)
if response.status_code == 200:
    data = response.json()
    location_name = data['location']['name']
    region = data['location']['region']
    country = data['location']['country']
    current = data['current']
    description = (
        f"Weather report for {location_name}, {region}, {country}:\n"
        f"- Temperature: {current['temp_c']}°C\n"
        f"- Condition: {current['condition']['text']}\n"
        f"- Wind Speed: {current['wind_kph']} kph\n"
        f"- Humidity: {current['humidity']}%\n"
        f"- Feels Like: {current['feelslike_c']}°C\n"
        f"- Last Updated: {current['last_updated']}\n"
    )
    print(description)
else:
       print(f"Failed to fetch weather data for '{location}': {response.status_code} {response.text}")

# city:str = "Lahore"
# result = requests.get(
#     f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
# )
# data = result.json()
# print(
#     f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
# )
