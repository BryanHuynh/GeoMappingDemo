import pandas as pd
import folium
from pprint import pprint
from geopy.geocoders import Nominatim

def CanadaMap(Provinces):
    nom = Nominatim(user_agent="http")
    geolocator = Nominatim(user_agent="http")

    #Provinces = ["British Columbia", "Alberta", "Saskatchewan", "Manitoba", "Ontario", "Quebec", "New Brunswick", "Nova Scotia", "Prince Edward Island", "Newfoundland and Labrador", "Northwest Territories", "Nunavut", "Yukon"]
    Country = "Canada"
    
    df = pd.DataFrame(columns=["Location Name", "Latitude", "Longitude", "geometry"])
    for province in Provinces:
        row = {"Location Name": province + ', ' + Country}
        df = pd.concat([df, pd.DataFrame(row, index=[0])])


    # loop through all provinces on df and append the geometry to the geometries list
    for index, row in df.iterrows():
        location = geolocator.geocode(row["Location Name"], geometry='geoJson')
        if location is not None:
            row["Latitude"] = location.latitude
            row["Longitude"] = location.longitude
            geoJson = location.raw['geojson']['coordinates'][0]
            # format data from [[],[]...] to [(),(),...]
            row["geometry"] = geoJson
        
    # pprint(df)


    canada_map = folium.Map(location=[51.0486, -114.0708], zoom_start=3)
    feature_layer = folium.FeatureGroup(name="Provinces")
    feature_layer.add_to(canada_map)
            

    for indew, row in df.iterrows():
        if row["geometry"] is not None:
            geoJson = row["geometry"]
            if type(geoJson[0][0]) == list:
                print('list item')
                for island in geoJson:
                    island = [(x[1],x[0]) for x in island]
                    folium.Polygon( island, 
                                    color='red', 
                                    weight=5, 
                                    fill=True, 
                                    fill_color='green',
                                    fill_opacity=0.5).add_to(feature_layer)
            else:
                # format data from [[],[]...] to [(),(),...]
                geoJson = [(x[1],x[0]) for x in geoJson]
                folium.Polygon( geoJson, 
                                color='red', 
                                weight=5, 
                                fill=True, 
                                fill_color='green',
                                fill_opacity=0.5).add_to(feature_layer)
        # add marker for that province
        folium.Marker(location=[row["Latitude"], row["Longitude"]],
                    popup=row["Location Name"],
                    icon=folium.Icon(color='blue', icon='info-sign')).add_to(feature_layer)




    folium.LayerControl().add_to(canada_map)

    canada_map.save('canada_map.html')
    # return html map
    return canada_map._repr_html_()