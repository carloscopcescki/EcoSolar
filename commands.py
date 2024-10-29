import folium
import streamlit as st
from streamlit_folium import st_folium
from typing import Any
from opencage.geocoder import OpenCageGeocode
from pvlib.location import Location
from pvlib import irradiance
import pandas as pd
import plotly.graph_objects as go
import math

class Geolocator:
    '''Class to return geolocalization with cache'''
    _cache: dict[Any, Any] = {}

    def __init__(self, location: str) -> None:
        self.location = location

    def result(self) -> Any:
        if self.location in self._cache:
            return self._cache[self.location]

        key = "4892bb222a594a99a1e75447a3ae333d"
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
        m = folium.Map(location=[self.latitude, self.longitude], zoom_start=18)

        tile = folium.TileLayer(
            tiles=
            'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            control=True,
            max_zoom=19).add_to(m)

        folium.LayerControl().add_to(m)
        st_data = st_folium(m, width=580, height=380)

        return None


class EnergyCalculate:
    '''Class to calculate energy potential and solar panel potential'''

    def __init__(self, panel_potential: float, module_quantity: int) -> None:
        self.panel_potential = panel_potential
        self.module_quantity = module_quantity

    def generate(self, irradiation: float,
                 efficiency: float, days: int) -> float | int:
        '''Calculate energy generated'''
        self.irradiation = irradiation
        self.efficiency = efficiency
        self.days = days

        self.media_efficiency = self.efficiency / 100
        media_potential = self.panel_potential / 1000
        energy = media_potential * self.irradiation * self.media_efficiency * self.days
        self.energy_rounded = round(energy, 2)

        return self.energy_rounded

    def capacity(self) -> float | int:
        '''Return solar panel system capacity'''
        self.sys_capacity = self.module_quantity * self.energy_rounded
        self.capacity_rounded = round(self.sys_capacity, 2)
        return self.capacity_rounded

    def payback(self, cost_kwh: float, system_capacity_kw: float, total_cost: float, hours: int) -> float | int:
        '''Calculate payback period for the solar panel system'''
        self.cost_kwh = cost_kwh
        self.system_capacity_kw = system_capacity_kw
        self.total_cost = total_cost
        self.hours = hours
        
        daily_energy = system_capacity_kw * hours
        monthly_energy = daily_energy * 30
        monthly_economy = monthly_energy * cost_kwh
        annual_economy = monthly_economy * 12

        payback_sys = total_cost / annual_economy
        return math.floor(payback_sys)

    def energy_generated_chart(self, latitude: float, longitude: float,
                               azimuth: float, tilt: float) -> Any:
        '''Generated solar energy chart '''
        self.latitude = latitude
        self.longitude = longitude
        self.azimuth = azimuth
        self.tilt = tilt

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
            dhi=irradiation_data['dhi'])

        hourly_production = (poa_irrad['poa_global'] / 1000) * (
            self.panel_potential / 1000) * self.efficiency
        daily_production = hourly_production.resample('D').sum()
        monthly_production = daily_production.resample('M').sum() / 100

        months = {
            'January': 'Janeiro',
            'February': 'Fevereiro',
            'March': 'Março',
            'April': 'Abril',
            'May': 'Maio',
            'June': 'Junho',
            'July': 'Julho',
            'August': 'Agosto',
            'September': 'Setembro',
            'October': 'Outubro',
            'November': 'Novembro',
            'December': 'Dezembro'
        }

        monthly_production.index = monthly_production.index.strftime('%B').map(
            months)

        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=monthly_production.index,
                   y=monthly_production.values,
                   name="Produção de Energia Solar (kWh)",
                   marker_color='#880808'))

        fig.update_layout(
            title_text='Produção de Energia Solar Estimada (kWh)',
            xaxis=dict(title='Mês', type='category', tickformat='.0f'),
            yaxis=dict(title='Energia (kWh)', tickformat='.0f',
                       ticksuffix='k'))

        return st.plotly_chart(fig)
