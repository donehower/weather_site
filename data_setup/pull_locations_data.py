import json
import requests
# import sys
# if sys.version_info[0] < 3:
#     from StringIO import StringIO
# else:
#     from io import StringIO

# --------------------------------------------- #
#   National Weather Service API Documentation:
#  https://forecast-v3.weather.gov/documentation
# ---------------------------------------------- #
us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'}


def get_locations():
    res = requests.get('https://api.weather.gov/stations')
    res = res.content.decode("utf-8")

    stations = json.loads(res)
    stations_data = stations['features']

    locations = {}
    for i in range(len(stations_data)):
        name = stations_data[i]['properties']['name']
        coord = stations_data[i]['geometry']['coordinates']
        id = stations_data[i]['properties']['stationIdentifier']
        locations.update({name: (coord, id)})

    return locations


def create_location_details(locations):
    counter = 1
    location_details = []
    failed_locations = []

    base_url = 'https://api.weather.gov/points/'
    for each in list(locations.keys()):
        full_url = base_url + str(locations[each][0][1]) + ',' + str(locations[each][0][0])
        res = requests.get(full_url)
        res = res.content.decode("utf-8")
        res = json.loads(res)

        try:
            station_id = locations[each][1]
            city = res['properties']['relativeLocation']['properties']['city']
            state_short = res['properties']['relativeLocation']['properties']['state']
            forecast_url = res['properties']['forecast']
            hourForecast_url = res['properties']['forecastHourly']
            coord = locations[each][0]

            location_details.append({'name': each,
                                     'city': city,
                                     'state_short': state_short,
                                     'state_full': us_state_abbrev[state_short],
                                     'station_id': station_id,
                                     'forecast_url': forecast_url,
                                     'hourForecast_url': hourForecast_url,
                                     'coord': coord})
            print("Count " + str(counter) + ": " + each)
            counter += 1
        except KeyError:
            failed_locations.append(each)
            print("Failed: " + each)

    return location_details, failed_locations


locations = get_locations()
final_details, failed_locations = create_location_details(locations)

with open('locations_details_v2.txt', 'w') as f:
    json.dump(final_details, f)
