import streamlit as st
from commands import *
from geopy.geocoders import Nominatim

def main() -> None:
    '''Create dashboard page'''
    st.set_page_config(
        page_title='Solar Dash',
        page_icon=':sunrise:',
        layout='wide'
    )
    
    geolocator = Nominatim(user_agent="geoapiExercises")
        
    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.title("FSA - Solar Dash")
    st.sidebar.write("Dashboard desenvolvido para auxiliar na pesquisa e estudo acerca do potencial energético solar da FSA e a viabilidade de implementação dos painéis solares.")
    st.sidebar.divider()

    # Input values
    st.sidebar.title("Inserir dados")
    search_location = st.sidebar.text_input("Buscar localização")
    panel_potencial = st.sidebar.number_input("Potência do painel solar (em kW)", min_value=0)
    solar_irradiation = st.sidebar.number_input("Irradiação solar (em kWh/m².dia)", min_value=0)
    system_efficiency = st.sidebar.number_input("Eficiência do sistema (%)", min_value=0, max_value=100, step=5)
    irradiation_days = st.sidebar.number_input("Número de dias", min_value=1, max_value=365, step=1)
    
    # Main elements
    col1, col2 = st.columns(2)
    
    with col1:
        st.title("Dados")
    with col2:
        st.title("Mapa")
        if search_location == "":
            st.warning("Insira um endereço no campo localização")
        else:
            local = geolocator.geocode(search_location)
            location = Map(local.latitude, local.longitude)
            location.map_generate()

if __name__ == "__main__":
    main()