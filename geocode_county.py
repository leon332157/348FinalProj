import pandas as pd

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="info348",timeout=5)  # you may need a timeout argument here!

county_data = pd.read_csv('county_proprietary_valid_2000_2018.csv')
loc= geolocator.geocode(f"{county_data['county'][0]}, {county_data['state'][0]}")

county_dict = {}
for i in range(len(county_data)):
    cty = county_data['county'][i]
    st = county_data['state'][i]
    adr = f"{cty}, {st}"
    if adr in county_dict:
        continue
    loc = geolocator.geocode(f"{cty}, {st}")
    if loc:
        county_dict[adr] = [loc.latitude, loc.longitude]
    else:
        county_dict[adr] = [0,0]

county_data['lat'] = county_data.apply(lambda row: county_dict[f"{row['county']}, {row['state']}"][0], axis=1)
county_data['lon'] = county_data.apply(lambda row: county_dict[f"{row['county']}, {row['state']}"][1], axis=1)
county_data.to_csv('county_data_geolocate.csv', index=False)