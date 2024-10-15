from lib2to3.pytree import convert
import folium
import streamlit as st
from streamlit_folium import st_folium
from typing import Any
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
import pvlib
from pvlib.location import Location
from pvlib import irradiance
import pandas as pd
import plotly.graph_objects as go
import locale

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
            self._cache[self.location] = result[0]
        
        return result[0] if result else None

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
    
    def energy_generated_chart(self, latitude: float, longitude: float, azimuth: float, tilt: float) -> Any:
        '''Generated solar energy chart '''
        self.latitude = latitude
        self.longitude = longitude
        self.azimuth = azimuth
        self.tilt = tilt
        
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        
        site = Location(latitude, longitude, tz='America/Sao_Paulo')
        times = pd.date_range('2024-01-01', '2024-12-31', freq='H', tz=site.tz)
        solar_position = site.get_solarposition(times)
        irradiation_data = site.get_clearsky(times)
        
        poa_irrad = irradiance.get_total_irradiance(
            surface_tilt=self.tilt,
            surface_azimuth=self.azimuth,
            solar_zenith=solar_position['apparent_zenith'],
            solar_azimuth=solar_position['azimuth'],
            dni=irradiation_data['dni'],
            ghi=irradiation_data['ghi'],
            dhi=irradiation_data['dhi']
        )
        
        hourly_production = (poa_irrad['poa_global'] / 1000) * (self.panel_potential / 1000) * self.efficiency
        daily_production = hourly_production.resample('D').sum()
        monthly_production = daily_production.resample('M').sum()
        monthly_production.index = monthly_production.index.strftime('%B')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_production.index,
            y=monthly_production.values,
            name="Produção de Energia Solar (kWh)",
            marker_color='#6495ED'
        ))

        fig.update_layout(
            title_text='Produção de Energia Solar',
            xaxis=dict(title='Mês', type='category'),
            yaxis=dict(title='Energia (kWh)')
        )
        
        return st.plotly_chart(fig)
