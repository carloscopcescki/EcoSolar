import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from commands import *

# Importar a biblioteca GSEE para fazer os cálculos do painel fotovoltaico
def main() -> None:
    '''Create dashboard page'''
    st.set_page_config(page_title='EcoSolar', page_icon='☀️', layout='wide')

    st.html('''
        <style>
        hr {
            border-color: #880808;
        }
        </style>
        ''')

    st.markdown(
        """
        <div style="background-color:#880808";padding:10px;border-radius:20px">
        <h1 style="color:white;text-align:center;">EcoSolar</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.image('./img/ecosolar.png', width=180)
    st.sidebar.subheader("")

    # Input values
    search_location = st.sidebar.text_input(
        "Pesquise um endereço",
        placeholder="Insira uma localização",
        value="FSA - Anexo II")

    panel_qty = st.sidebar.slider("Quantidade de painéis solares", 1, 400, 20)
    panel_potencial = st.sidebar.number_input("Potência do painel solar (Wp)",
                                              min_value=0.0,
                                              value=400.0)
    #module_efficiency = st.sidebar.number_input("Eficiência do módulo (%)", min_value=0.0, max_value=100.0, step=0.1, value=20.2, format='%f') / 100
    solar_irrad_generate = st.sidebar.number_input(
        "Irradiação solar (kWh/m².dia)", min_value=0.0, value=4.53)
    sys_efficiency_generate = st.sidebar.number_input(
        "Desempenho do sistema (%)",
        key='efficiency-generated',
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        value=75.0)
    day_generate = st.sidebar.number_input("Número de dias",
                                           key='days-generated',
                                           min_value=1,
                                           max_value=365,
                                           step=1,
                                           value=365)
    tilt = st.sidebar.slider("Inclinação do painel solar (°)", 0.0, 90.00,
                             24.00)
    azimuth = st.sidebar.slider("Orientação do painel (°)", -180, 180, 0)

    st.sidebar.divider()
    st.sidebar.subheader("Payback")
    #energy_consumption = st.sidebar.number_input("Consumo anual de energia (kWh)", key='consumption', min_value=0, value=3000)
    cost_install = st.sidebar.number_input("Custo de instalação (R$)", key='cost_install', min_value=0.0, value=44000.00)
    cost_kwh = st.sidebar.number_input("Custo por kWh (R$)",
                                       key='cost_kwh',
                                       min_value=0.0,
                                       value=0.65)

    sun_hours = st.sidebar.number_input("Quantidade de horas de sol pleno", key='sun_hours', min_value=1, max_value=24, value=4, step=1)
    
    system_capacity_kw = ((panel_qty * panel_potencial) / 1000)
    
    # Main elements
    calculate = EnergyCalculate(panel_potencial, panel_qty)
    location = Geolocator(search_location)
    result = location.result()
    st.divider()
    st.subheader("Dados")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Energia gerada por painel",
        value=
        f"{calculate.generate(solar_irrad_generate, sys_efficiency_generate, int(day_generate))}kWh"
    )
    col2.metric(label="Capacidade gerada pelo sistema",
                value=f"{calculate.capacity()}kWh")
    col3.metric(label="Quantidade de painéis", value=panel_qty)
    col4.metric(label="Payback aproximado",
                value=f"{calculate.payback(cost_kwh, system_capacity_kw, cost_install, int(sun_hours))} anos")
    style_metric_cards(background_color="#0E1117",
                       border_left_color='#880808',
                       border_color='#880808')

    # Map
    col1a, col2a, col3a = st.columns([2.5, 0.2, 2])

    # Solar energy production chart
    with col1a:
        st.subheader("Energia gerada")
        if result and search_location != "FSA - Anexo II":
            lat, lon = result['geometry']['lat'], result['geometry']['lng']
            energy_chart = calculate.energy_generated_chart(
                lat, lon, azimuth, tilt)
        else:
            energy_chart = calculate.energy_generated_chart(
                -23.6622, -46.5541, azimuth, tilt)

    with col3a:
        st.subheader(f"Mapa {search_location}")
        if search_location == "":
            st.warning("Insira um endereço no campo localização")
        else:
            if result and search_location != "FSA - Anexo II":
                lat, lon = result['geometry']['lat'], result['geometry']['lng']
                map_location = Map(lat, lon)
                map_location.map_generate()
            else:
                fsa_lat = '-23.6622'
                fsa_lon = '-46.5541'
                map_location = Map(fsa_lat, fsa_lon)
                map_location.map_generate()

    st.divider()

if __name__ == "__main__":
    main()
