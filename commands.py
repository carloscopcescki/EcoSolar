import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
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
            border-color: #6495ED;
            border-radius: 100px;
        }
        </style>
        '''
    )
    
    key = st.secrets["secrets"]["api"]
    geocoder = OpenCageGeocode(key)
        
    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.image('./img/fsa.png', width=250)
    st.sidebar.title("Solar Dash")
    st.sidebar.write("Dashboard desenvolvido para auxiliar na pesquisa e estudo acerca do potencial energético solar da FSA e a viabilidade de implementação dos painéis solares.")
    
    # Input values
    st.sidebar.title("Inserir dados")
    search_location = st.sidebar.text_input("Pesquise um endereço", placeholder="Insira uma localização", value="FSA - Anexo II")

    with st.sidebar.expander("Energia gerada"):
        st.info("Calcular a quantidade de energia gerada por painel solar")
        panel_qty = st.slider("Painéis solares", 0, 150, 1)
        panel_potencial = st.number_input("Potência do painel solar (em kWh)", min_value=0, value=400)
        solar_irrad_generate = st.number_input("Irradiação solar (em kWh/m².dia)", min_value=0.0, value=4.53)
        energy_consumption = st.number_input("Consumo médio mensal de energia (em kWh)", min_value=0, value=550)
        sys_efficiency_generate = st.number_input("Eficiência do sistema (%)", key='efficiency-generated', min_value=0, max_value=100, step=5, value=80)
        cost_kwh = st.number_input("Custo por kWh")
        day_generate = st.number_input("Número de dias", key='days-generated', min_value=1, max_value=365, step=1, value=30)

    # Main elements
    st.title("Solar Dash")
    
    col1, col2, col3, col4 = st.columns(4)
    
    calculate = EnergyCalculate()
    
    col1.metric(label="Energia gerada por painel", value=f"{calculate.generate(panel_potencial, solar_irrad_generate, sys_efficiency_generate, int(day_generate))}kWh")
    col2.metric(label="Capacidade gerada pelo sistema", value=f"{calculate.capacity(panel_qty)}kWh")
    col3.metric(label="Quantidade de painéis", value=panel_qty)
    col4.metric(label="Custo", value=f"R$ {5000}")
    style_metric_cards(border_left_color='#6495ED')

    st.divider()
    st.header("Mapa")
    
    if search_location == "":
        st.warning("Insira um endereço no campo localização")
    else:
        result = geocoder.geocode(search_location)
        if result and search_location != "FSA - Anexo II":
            location = result[0]['geometry']
            lat, lon = location['lat'], location['lng']
            map_location = Map(lat, lon)
            map_location.map_generate()
        else:
            fsa_lat = '-23.6622'
            fsa_lon = '-46.5541'
            map_location = Map(fsa_lat, fsa_lon)
            map_location.map_generate()

if __name__ == "__main__":
    main()
