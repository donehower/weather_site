import requests
import json


def get_current_conditions(station_id):

    url_1 = 'https://api.weather.gov/stations/'
    station_id = station_id
    url_2 = '/observations/current'

    url_full = url_1 + station_id + url_2

    # create HTTP response object from given url
    res = requests.get(url_full)

    res = res.content.decode('utf-8', 'ignore')
    res = json.loads(res)

    dir_index = {'1': 'N', '2': 'NNE', '3': 'NE', '4': 'ENE', '5': 'E',
                 '6': 'ESE', '7': 'SE', '8': 'SSE', '9': 'S', '10': 'SSW',
                 '11': 'SW', '12': 'WSW', '13': 'W', '14': 'WNW', '15': 'NW',
                 '16': 'NNW', '17': 'N', '18': ' '}

    def degree_to_cardinal(degree):
        if degree is ' ':
            return dir_index['18']
        else:
            temp_var = round((degree % 360) / 22.5) + 1
            temp_var = str(temp_var)
            return dir_index[temp_var]

    def c_to_f(tc):
        return round(tc * (9/5) + 32)

    def feels_like(windChill, heatIndex):
        if windChill is None:
            return None
        elif heatIndex is None:
            return None
        elif windChill is not None:
            windChill = c_to_f(windChill)
            return str(round(windChill))
        elif heatIndex is not None:
            heatIndex = c_to_f(heatIndex)
            return str(round(heatIndex))

    # Descriptive Conditions
    text_conditions = res['properties']['textDescription']
    # Temperature (reported as celsius and converted to fahrenheit)
    tc = res['properties']['temperature']['value']
    tf = c_to_f(tc)
    # Wind direction and speed (converted from m/s to mph)
    windD_deg = res['properties']['windDirection']['value']
    if windD_deg is type(None):
        windD_deg = ' '
    if windD_deg is not type(None):
        windD_deg = round(windD_deg)

    windD_card = degree_to_cardinal(windD_deg)
    windS = res['properties']['windSpeed']['value']
    if windS is type(None):
        windS = ' '
    if windS is not type(None):
        windS = windS * 2.236936
    #Relative Humidity
    relH = round(res['properties']['relativeHumidity']['value'])
    # Wind chill and heat index
    windChill = res['properties']['windChill']['value']
    heatIndex = res['properties']['heatIndex']['value']
    feels_like = feels_like(windChill, heatIndex)

    conditions = {'descrip': text_conditions, 'temp': tf,
                  'windD_deg': windD_deg, 'windD_card': windD_card,
                  'windS': windS, 'relH': relH, 'feels_like': feels_like}

    return conditions
