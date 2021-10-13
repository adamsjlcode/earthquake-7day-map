import datetime
import json
import folium
import requests
import strict_rfc3339

FORMAT = ''

time = []
lat = []
lon = []
dept = []
mag = []
place = []
link = []

def wjsontfile(jsondata):
    with open('data.txt', 'w') as outfile:
        json.dump(jsondata, outfile)


starttime = '2020-03-07'
endtime = '2020-03-12'
response = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + starttime + "&endtime=" + endtime + "&minmagnitude=1")
jsonData = response.json()

for quake in jsonData['features']:
    lon.append(quake['geometry']['coordinates'][0])
    lat.append(quake['geometry']['coordinates'][1])
    dept.append(quake['geometry']['coordinates'][2])
    link.append(quake['properties']['detail'])
    time.append(quake['properties']['time'])
    mag.append(quake['properties']['mag'])
    place.append(quake['properties']['place'])


def color_producer(mag):
    if mag < 2.0:
        return 'green'
    elif 2.0 <= mag < 4.0:
        return 'orange'
    else:
        return 'red'


def load_marker(time, place, mag, dept, link):
    tm = (datetime.datetime.strftime(datetime.datetime.fromtimestamp(time/1000),'%B %m, %Y'))
    return (
            "<h1>Earthquake</h1><br>"
            "<h3>{}</h2><br>"
            "<p>Location: {}<br>"
            "Magnitude: {}<br>"
            "Depth: {}<br>"
            "<a href=\"{}\">Link</a></p>".format(tm,place,mag,dept,link)
            )
            # (
            # """
            # <h1>Earthquake</h1><br>
            # """
            # """
            # """
            # "<p>" +
            # "At " + read_parse_time(time) + '<br>' +
            # "Location: " + place + '<br>' +
            # "Magnitude: " + str(mag) +
            # "</p>"
            # )


def read_parse_time(rfc_time):
    time = datetime.datetime.fromtimestamp(strict_rfc3339.rfc3339_to_timestamp(rfc_time))
    return datetime.datetime.strftime(time, FORMAT)


map = folium.Map(location=[35.062511, -80.974479], zoom_start=8, tiles="Stamen Toner")
fgv = folium.FeatureGroup(name="Earthquakes")
for tm, lt, ln, mg, dep, pl, lk in zip(time, lat, lon, mag, dept, place, link):
    fgv.add_child(folium.CircleMarker(
        location=[lt, ln],
        radius=6,
        popup=load_marker(tm, pl, mg, dep, lk),
        fill=True,
        fill_color=color_producer(mg),
        color='gray',
        fill_opacity=0.7, ))
map.add_child(fgv)
map.save("Earthquakes.html")
