import streamlit as st
from streamlit_option_menu import option_menu
from views.home_page import pagina_inicial

# Configuração da página
st.set_page_config(
    page_title="Extratos da Terra",
    page_icon="🪷",
    layout="wide"
)

# Menu lateral estilizado com cores modernas
with st.sidebar:
    st.image(r"C:\Users\equip\Documents\dev\file.png", width=200)
     
    selected = option_menu(
        menu_title=" ",  # Sem título no topo
        options=["Página Inicial", "Vanessa", "Katllen", "Gabriel"],
        icons=["house", "person", "person", "person"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#524E4E"},  # fundo do menu
            "icon": {"color": "#8B5CF6", "font-size": "20px"},  # ícones roxo suave
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#C084FC"  # hover roxo claro
            },
            "nav-link-selected": {
                "background-color": "#8B5CF6",  # roxo forte
                "color": "white",
                "border-radius": "8px",
                "font-weight": "normal"# cantos arredondados para o selecionado
            },
        }
    )

# Navegação entre páginas
if selected == "Página Inicial":
    st.title("Extratos da Terra")
    pagina_inicial()
elif selected == "Vanessa":
    st.title("Relatório Vanessa")
elif selected == "Katllen":
    st.title("Relatório Katllen")
elif selected == "Gabriel":
    st.title("Relatório Gabriel")
