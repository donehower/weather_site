import requests
import json


def get_current_conditions(station_id):
    # create url for API call
    url_1 = 'https://api.weather.gov/stations/'
    station_id = station_id
    url_2 = '/observations/current'

    url_full = url_1 + station_id + url_2

    # create HTTP response object from given url
    res = requests.get(url_full)

    res = res.content.decode('utf-8', 'ignore')
    res = json.loads(res)

    # Dictionary for converting wind directions from degress to cardinal direction
    dir_index = {'1': 'N', '2': 'NNE', '3': 'NE', '4': 'ENE', '5': 'E',
                 '6': 'ESE', '7': 'SE', '8': 'SSE', '9': 'S', '10': 'SSW',
                 '11': 'SW', '12': 'WSW', '13': 'W', '14': 'WNW', '15': 'NW',
                 '16': 'NNW', '17': 'N', '18': ' '}

    # Methods for data conversions
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

    # Test whether a valid response was provided
    # Return zero if API response held not valid data
    has_response = res.get('properties', 0)
    if has_response == 0:
        return 0;
    else:
        # Descriptive Conditions
        text_conditions = res['properties']['textDescription']
        if isinstance(text_conditions, str):
            text_conditions = text_conditions
        else:
            text_conditions = " "

        # Temperature (reported as celsius and converted to fahrenheit)
        tc = res['properties']['temperature']['value']
        if isinstance(tc, float) or isinstance(tc, int):
            tf = c_to_f(tc)
        else:
            tf = "Unavailable"

        # Wind direction and speed (converted from m/s to mph)
        windD_deg = res['properties']['windDirection']['value']
        if isinstance(windD_deg, float) or isinstance(windD_deg, int):
            windD_deg = round(windD_deg)
            windD_card = degree_to_cardinal(windD_deg)
        else:
            windD_deg = "Unavailable"
            windD_card = "Unavailable"

        windS = res['properties']['windSpeed']['value']
        if isinstance(windS, float) or isinstance(windS, int):
            windS = windS * 2.236936
        else:
            windS = "Unavailable"

        #Relative Humidity
        relH = res['properties']['relativeHumidity']['value']
        if isinstance(relH, float) or isinstance(relH, int):
            relH = round(relH)
        else:
            relH = "Unavailable"

        # Wind chill and heat index
        windChill = res['properties']['windChill']['value']
        heatIndex = res['properties']['heatIndex']['value']
        if (isinstance(windChill, float) or isinstance(windChill, int)) and (isinstance(heatIndex, float) or isinstance(heatIndex, int)):
             feels_like = feels_like(windChill, heatIndex)
        else:
            feels_like = tf

        # Results to return as a dictionary
        conditions = {'descrip': text_conditions, 'temp': tf,
                      'windD_deg': windD_deg, 'windD_card': windD_card,
                      'windS': windS, 'relH': relH, 'feels_like': feels_like}
        # Check for number of unavailble values
        # Return zero if there are three or more "Unavailable values"
        conditions_vals = list(conditions.values())
        if conditions_vals.count("Unavailable") > 2:
            return 0
        else:
            return conditions
