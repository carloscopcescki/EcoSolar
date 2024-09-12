from lib2to3.pytree import convert
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
               zoom_start=18)

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
    
class EnergyCalculate:
    '''Class to calculate energy potential and solar panel potential'''
    def __init__(self) -> None:
        pass

    def generate(self, qty_panel: float, panel_potential: float, irradiation: float, efficiency: float, days: float) -> float:
        '''Calculate energy generated'''
        self.panel_potential = panel_potential
        self.irradiation = irradiation
        self.efficiency = efficiency
        self.days = days
        self.qty = qty_panel

        media_efficiency = self.efficiency / 100
        media_potential = self.panel_potential / 1000
        energy = media_potential * self.irradiation * media_efficiency * self.days
        energy_perpanel = energy * self.qty
        energy_rounded = round(energy_perpanel, 2)

        return energy_rounded

class Panel:
    '''Calculate panel solar system'''
    def __init__ (self) -> None:
        pass
        
    def systemCapacity(self, panel: float, consumption: float, irradiation: float, efficiency: float, days: float) -> float:
        '''Return solar panel system capacity'''
        self.panel = panel
        self.consumption = consumption
        self.irradiation = irradiation
        self.efficiency = efficiency
        self.days = days
        
        cons_day = self.consumption / self.days
        cons_irrad = cons_day / self.irradiation
        media_efficiency = self.efficiency / 100
        sys_capacity = cons_irrad / media_efficiency
        self.media_capacity = round(sys_capacity, 2)
        
        return self.media_capacity

    def quantity(self) -> float:
        '''Return solar panel quantity'''
        convert_sys = self.media_capacity * 1000
        qty = convert_sys / self.panel
        qty_rounded = round(qty, 1)
        
        return qty_rounded