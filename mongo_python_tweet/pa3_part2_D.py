import folium
import pandas as pd

colnames = ['text','user','created_at','geo','location']
dt = pd.read_csv('usa_tweets.csv',names=colnames)
data = dt.to_dict(orient='records')
map = folium.Map(location=[39.833333, -98.583333], zoom_start=4)
count = 0
for value in data:
    geo = value['geo']
    geo_data = geo[1:-1]
    if len(geo_data.split(", ")) == 2:
        geo_data1 = float(geo_data.split(", ")[0])
        geo_data2 = float(geo_data.split(", ")[1])
        folium.CircleMarker([geo_data1,geo_data2],
                            radius=2,
                            color='#3186cc',
                           ).add_to(map)
        count+=1
        print(count)

map.save('map.html')