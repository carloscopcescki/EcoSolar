import streamlit as st

def main():
    '''Create dashboard page'''
    st.set_page_config(
        page_title='Solar Panel',
        page_icon=':sunrise:',
        layout='wide'
    )
    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.image('./img/fsa.png', use_column_width=True)
    st.sidebar.title("FSA - Solar Dash")
    st.sidebar.write("Dashboard desenvolvido para exibir quantidade necessária de painés solares na FSA + potencial energético da região.")
    st.sidebar.divider()

    panel_potencial = st.sidebar.text_input("Potência do painel solar (em kW")
    solar_irradiation = st.sidebar.text_input("Irradiação solar (em kWh/m².dia)")
    system_efficiency = st.sidebar.text_input("Eficiência do sistema")
    irradiation_days = st.sidebar.number_input("Número de dias", min_value=1, max_value=365, step=1)

    # Main elements
    st.title("Irradiação Solar Média - Grande ABC")
    with open('mapa_interativo.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    st.components.v1.html(html_content, width=750, height=600)
    
if __name__ == "__main__":
    main()
