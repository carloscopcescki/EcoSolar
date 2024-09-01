import streamlit as st

class Dashboard:
    '''Inicialize dashboard'''
    def __init__(self) -> None:
        pass
    
    def page(self):
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
        
        # Main elements
        img1, img2 = st.columns(2)
        with img1:
            st.image('./img/Mapa-FSA-2024.jpg', width=650)
        with img2:
            st.image('./img/media_solar.png', width=425)