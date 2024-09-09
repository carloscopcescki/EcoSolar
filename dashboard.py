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
    
    
    # Main elements
    st.title("Irradiação Solar Média - Grande ABC")
    with open('irradiacao_media_abc.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    st.components.v1.html(html_content, width=600, height=450)
    
if __name__ == "__main__":
    main()
