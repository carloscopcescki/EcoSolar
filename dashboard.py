import streamlit as st
from commands import *
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode

def main() -> None:
    '''Create dashboard page'''
    st.set_page_config(
        page_title='Solar Dash',
        page_icon=':sunrise:',
        layout='wide'
    )
    
    st.html(
        '''
        <style>
        hr {
            border-color: blue;
            border-radius: 100px;
        }
        </style>
        '''
    )
    
    key = st.secrets['api_key']
    
    geocoder = OpenCageGeocode(key)
        
    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.image('./img/fsa.png')
    st.sidebar.title("Solar Dash")
    st.sidebar.write("Dashboard desenvolvido para auxiliar na pesquisa e estudo acerca do potencial energético solar da FSA e a viabilidade de implementação dos painéis solares.")

    # Input values
    st.sidebar.title("Inserir dados")
    search_location = st.sidebar.text_input("Pesquise um endereço", placeholder="Insira uma localização", value="Fundação Santo André")

    with st.sidebar.expander("Energia gerada"):
        st.info("Calcular a quantidade de energia gerada por painel solar")
        panel_qty = st.slider("Painéis solares", 0, 150, 1)
        panel_potencial = st.number_input("Potência do painel solar (em kWh)", min_value=0)
        solar_irrad_generate = st.number_input("Irradiação solar (em kWh/m².dia)", min_value=0.0, value=4.00)
        sys_efficiency_generate = st.number_input("Eficiência do sistema (%)", key='efficiency-generated', min_value=0, max_value=100, step=5, value=80)
        day_generate = st.number_input("Número de dias", key='days-generated', min_value=1, max_value=365, step=1, value=30)

    with st.sidebar.expander("Quantidade de painéis solares"):
        st.info("Calcular a quantidade de painéis solares para o sistema")
        energy_consumption = st.number_input("Consumo médio mensal de energia (em kWh)", min_value=0, value=550)
        panel = st.number_input("Potência do painel solar (em kWh)", key="panel_potential", min_value=0, value=400)
        solar_irrad_panel = st.number_input("Irradiação solar (em kWh/m².dia)", key='irrad-panel', min_value=0.0, value=4.00)
        sys_efficiency_panel = st.number_input("Eficiência do sistema (%)", key='efficiency-panel', min_value=0, max_value=100, step=5, value=80)
        day_panel = st.number_input("Número de dias", key='days-panel', min_value=1, max_value=365, step=1, value=30)
    
    # Main elements
    st.title("Solar Dash")
    st.divider()
    col1, col2 = st.columns(2)
    
    col1.header('Dados')
    col2.header('Mapa')
    
    with col1:
        calculate = EnergyCalculate()
        panel_sys = Panel()

        col1a, col1b = st.columns(2)
        with col1a:
            st.image('./img/tomada.jpg', width=200)
            st.text(f"Energia gerada: {calculate.generate(panel_qty, panel_potencial, solar_irrad_generate, sys_efficiency_generate, int(day_generate))}kWh")
        with col1b:
            st.image('./img/system.jpg', width=200)
            st.text(f"Capacidade do sistema: {panel_sys.capacity(panel, energy_consumption, solar_irrad_panel, sys_efficiency_panel, int(day_panel))}kW")
        
        col2a, col2b = st.columns(2)
        with col2a:
            st.image('./img/solar_panel.png', width=200)
            st.text(f"Quantidade de painéis: {panel_sys.quantity()}")

    with col2:
        if search_location == "":
            st.warning("Insira um endereço no campo localização")
        else:
            result = geocoder.geocode(search_location)
            if result:
                location = result[0]['geometry']
                lat, lon = location['lat'], location['lng']
                map_location = Map(lat, lon)
                map_location.map_generate()

if __name__ == "__main__":
    main()