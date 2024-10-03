from lib2to3.pytree import convert
import folium
from streamlit_folium import st_folium
from typing import Any
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode

class Geolocator:
    '''Class to return geolocalization with cache'''
    _cache: dict[Any, Any] = {}

    def __init__(self, location: str) -> None:
        self.location = location

    def result(self) -> Any:
        if self.location in self._cache:
            return self._cache[self.location]
        
        key = st.secrets["secrets"]["api"]
        geocoder = OpenCageGeocode(key)

        result = geocoder.geocode(self.location)
        
        if result:
            self._cache[self.location] = result
        
        return result

class Map:
    '''Class to generate map and extract coordinates'''
    def __init__(self, latitude: str, longitude: str) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def map_generate(self) -> Any: 
        '''Generate map'''
        m = folium.Map(location=[self.latitude, self.longitude], 
               zoom_start=18)

        tile = folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            control=True,
            max_zoom=19
        ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_data = st_folium(m, width=800, height=620)
        
        return None

class EnergyCalculate:
    '''Class to calculate energy potential and solar panel potential'''
    def __init__(self) -> None:
        pass

    def generate(self, panel_potential: float, irradiation: float, efficiency: float, days: int) -> float | int:
        '''Calculate energy generated'''
        self.panel_potential = panel_potential
        self.irradiation = irradiation
        self.efficiency = efficiency
        self.days = days

        media_efficiency = self.efficiency / 100
        media_potential = self.panel_potential / 1000
        energy = media_potential * self.irradiation * media_efficiency * self.days
        self.energy_rounded = round(energy, 2)

        return self.energy_rounded

    def capacity(self, qty_panel: int) -> float | int:
        '''Return solar panel system capacity'''
        self.qty = qty_panel
        self.sys_capacity = self.qty * self.energy_rounded
        self.capacity_rounded = round(self.sys_capacity, 2)
        return self.capacity_rounded

    def payback(self, cost_sys: float, cost_kwh: float) -> float:
        '''Calculate solar panel system cost'''
        self.cost_system = cost_sys
        self.cost_kwh = cost_kwh
        
        payback_sys = (self.cost_system / (self.sys_capacity * 12 * self.cost_kwh))
        payback_rounded = int(payback_sys)
        return payback_rounded
