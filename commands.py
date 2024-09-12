import folium
from streamlit_folium import st_folium
from typing import Any

class Map:
    '''Class to generate map and extract coordinates'''
    def __init__(self, latitude: str, longitude: str) -> None:
        self.latitude = latitude
        self.longitude = longitude
    
    def map_generate(self) -> Any: 
        '''Generate map'''
        m = folium.Map(location=[self.latitude, self.longitude], 
               zoom_start=17)

        tile = folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_data = st_folium(m, width=725)
        
        return st_data
    
class Geolocation:
    def __init__(self) -> None:
        pass