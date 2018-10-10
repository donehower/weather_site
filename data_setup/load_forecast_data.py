import requests
import xmltodict
from datetime import datetime, timedelta

# get start and end dates for api request
today = datetime.today()
today_plus_5 = today + timedelta(days=6)

today = today.strftime('%Y-%m-%d')
today_plus_5 = today_plus_5.strftime('%Y-%m-%d')

# create the url for request
url_a = 'https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?whichClient=NDFDgenMultiCities&lat=&lon=&listLatLon=&lat1=&lon1=&lat2=&lon2=&resolutionSub=&listLat1=&listLon1=&listLat2=&listLon2=&resolutionList=&endPoint1Lat=&endPoint1Lon=&endPoint2Lat=&endPoint2Lon=&listEndPoint1Lat=&listEndPoint1Lon=&listEndPoint2Lat=&listEndPoint2Lon=&zipCodeList=&listZipCodeList=&centerPointLat=&centerPointLon=&distanceLat=&distanceLon=&resolutionSquare=&listCenterPointLat=&listCenterPointLon=&listDistanceLat=&listDistanceLon=&listResolutionSquare=&citiesLevel=1234&listCitiesLevel=&sector=&gmlListLatLon=&featureType=&requestedTime=&startTime=&endTime=&compType=&propertyName=&product=time-series&begin='
url_start_date = today
url_b = 'T00%3A00%3A00&end='
url_end_date = today_plus_5
url_c = 'T00%3A00%3A00&Unit=e&temp=temp&pop12=pop12&wspd=wspd&wdir=wdir&sky=sky&rh=rh&Submit=Submit'

full_url = url_a + url_start_date + url_b + url_end_date + url_c

# create HTTP response object from given url
resp = requests.get(full_url)
resp = resp.content.decode("utf-8")

# parse xml object into json-like structure
raw = xmltodict.parse(resp)

# create a dictionary of all data reporting time_schedules
time_schedules = raw['dwml']['data']['time-layout']
sched_dict = {}
for each in time_schedules:
    sched_dict.update({each['layout-key']: each['start-valid-time']})

# create dictionary of data
# key: city
# value: location-key,
#        state,
#        temperature: {sched, values},
#        wind-speed: {sched, values},
#        direction: {sched, values},
#        cloud-amount: {sched, values},
#        probability-of-precipitation: {sched, values},
#        humidity: {sched, values}
all_data = {}
for i in range(len(raw['dwml']['data']['parameters'])):
    all_data.update({raw['dwml']['data']['location'][i]['city']['#text']:
                     {'location-key': raw['dwml']['data']['location'][i]['location-key'],
                      'state': raw['dwml']['data']['location'][i]['city']['@state'],
                      'temperature': {'sched': sched_dict[raw['dwml']['data']['parameters'][i]['temperature']['@time-layout']],
                                      'values': raw['dwml']['data']['parameters'][i]['temperature']['value']},
                      'wind-speed': {'sched': sched_dict[raw['dwml']['data']['parameters'][i]['wind-speed']['@time-layout']],
                                     'values': raw['dwml']['data']['parameters'][i]['wind-speed']['value']},
                      'direction': {'sched': sched_dict[raw['dwml']['data']['parameters'][i]['direction']['@time-layout']],
                                    'values': raw['dwml']['data']['parameters'][i]['direction']['value']},
                      'cloud-amount': {'sched': sched_dict[raw['dwml']['data']['parameters'][i]['cloud-amount']['@time-layout']],
                                       'values': raw['dwml']['data']['parameters'][i]['cloud-amount']['value']},
                      'probability-of-precipitation': {'sched': sched_dict[raw['dwml']['data']['parameters'][i]['probability-of-precipitation']['@time-layout']],
                                                       'values': raw['dwml']['data']['parameters'][i]['probability-of-precipitation']['value']},
                      'humidity': {'sched': sched_dict[raw['dwml']['data']['parameters'][i]['humidity']['@time-layout']],
                                   'values': raw['dwml']['data']['parameters'][i]['humidity']['value']}}})
all_data['Oklahoma City']['temperature']
