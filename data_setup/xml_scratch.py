import requests
import json

url = 'https://api.weather.gov/stations/KLAX/observations/current'

# create HTTP response object from given url
res = requests.get(url)

res = res.content.decode('utf-8', 'ignore')
res = json.loads(res)


def c_to_f(tc):
    return tc * (9/5) + 32


conditions = res['properties']['textDescription']
tc = res['properties']['temperature']['value']
# convert temp to Fahrenheit
tf = c_to_f(tc)
windD = res['properties']['windDirection']['value']
windS = res['properties']['windSpeed']['value']
# convert meters per second to miles per hour
windS = res['properties']['windSpeed']['value'] * 2.236936
relH = res['properties']['relativeHumidity']['value']
windChill = res['properties']['windChill']['value']
if windChill is not None:
    windChill = c_to_f(windChill)
heatIndex = res['properties']['heatIndex']['value']
if heatIndex is not None:
    heatIndex = c_to_f(heatIndex)
heatIndex
