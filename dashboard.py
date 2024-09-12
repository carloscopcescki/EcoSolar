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
    
    geolocator = Nominatim(user_agent="geoapiExercises", timeout=None)
        
    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.title("Solar Dash")
    st.sidebar.write("Dashboard desenvolvido para auxiliar na pesquisa e estudo acerca do potencial energético solar da FSA e a viabilidade de implementação dos painéis solares.")

    # Input values
    st.sidebar.title("Inserir dados")
    search_location = st.sidebar.text_input("Buscar localização")

    with st.sidebar.expander("Energia gerada"):
        st.info("Calcular a quantidade de energia gerada por painel solar")
        panel_qty = st.slider("Quantidade de painéis", 0, 150, 1)
        panel_potencial = st.number_input("Potência do painel solar (em kWh)", min_value=0)
        solar_irrad_generate = st.number_input("Irradiação solar (em kWh/m².dia)", min_value=0.0)
        sys_efficiency_generate = st.number_input("Eficiência do sistema (%)", key='efficiency-generated', min_value=0, max_value=100, step=5)
        day_generate = st.number_input("Número de dias", key='days-generated', min_value=1, max_value=365, step=1)

    with st.sidebar.expander("Quantidade de painéis solares"):
        st.info("Obter a quantidade de painéis solares para um sistema fotovoltaico")
        energy_consumption = st.number_input("Consumo médio mensal de energia (em kWh)", min_value=0)
        panel = st.number_input("Potência do painel solar escolhido (em kWh)", min_value=0)
        solar_irrad_panel = st.number_input("Irradiação solar (em kWh/m².dia)", key='irrad-panel', min_value=0.0)
        sys_efficiency_panel = st.number_input("Eficiência do sistema (%)", key='efficiency-panel', min_value=0, max_value=100, step=5)
        day_panel = st.number_input("Número de dias", key='days-panel', min_value=1, max_value=365, step=1)
    
    bt_calc = st.sidebar.button("Calcular")

    # Main elements
    col1, col2 = st.columns(2)
    
    with col1:
        st.title("Dados")
        if bt_calc:
            calcular = EnergyCalculate()
            response_energy = calcular.energyGenerate(panel_qty, panel_potencial, solar_irrad_generate, sys_efficiency_generate, day_generate)
            st.subheader(f"Energia gerada: {response_energy}kWh")
            
            st.divider()

            panel = SolarSystem(panel, energy_consumption, solar_irrad_panel, sys_efficiency_panel, day_panel)
            st.subheader(f"Capacidade do sistema: {panel.systemCapacity()}kW")
            st.subheader(f"Quantidade necessária: {panel.quantity()} painéis solares.")

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