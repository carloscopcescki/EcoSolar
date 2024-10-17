def energy_generated_chart(self, latitude: float, longitude: float, azimuth: float, tilt: float) -> Any:
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
            dhi=irradiation_data['dhi']
        )

        hourly_production = (poa_irrad['poa_global'] / 1000) * (self.panel_potential / 100) * self.efficiency
        daily_production = hourly_production.resample('D').sum()
        monthly_production = daily_production.resample('M').sum()

        months = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
            'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
            'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }

        monthly_production.index = monthly_production.index.strftime('%B').map(months)

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
