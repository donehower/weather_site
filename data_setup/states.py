import csv

st_abbr_list = []
with open('/Users/sarahdonehower/Documents/projects/weather_site/data_setup/state_abbr.csv', encoding='utf-8-sig') as f:
    csv_reader = csv.reader(f, strict=False)
    for row in csv_reader:
        st_abbr_list.append((row[1], row[0]))
