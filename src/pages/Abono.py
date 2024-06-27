import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

#### Config ####
st.set_page_config(page_title="Abono Permanência",
                   page_icon="🕗", layout="wide")

##### State ####
if "abono" not in st.session_state:
    st.session_state["abono"] = None

abono = st.session_state["abono"]


def set_menu():
    """
    Função para configurar a sidebar

    """
    with st.sidebar:
        st.title("Menu Abono Permanência")

        selected_page = option_menu(
            menu_title=None,
            options=["Dashboard 01", "Dashboard 02", "Dashboard 03"],
            icons=["receipt-cutoff", "graph-up-arrow", "bar-chart"],
            orientation="vertical",
        )

    return selected_page


def main():

    if abono is None:
        st.write(
            "Por favor, faça o upload do arquivo com os dados do Abono Permanência")
        return

    selected_page = set_menu()

    if selected_page == "Dashboard 01":
        st.title("Dashboard 01")
        st.metric(label="Quantidade de Servidores",
                  value=abono.qtd_servidores_abono_permanencia(), delta="1.23%")

        st.markdown("---")
        abono_por_uf = abono.qtd_servidores_abono_permanencia_por_uf_residencia()

        fig = px.bar(abono_por_uf, x=abono_por_uf.index, y=abono_por_uf.values,
                     title="Quantidade de Servidores com Abono Permanência por UF")
        st.plotly_chart(fig)

        st.markdown("---")

        cols = st.columns(4)

        with cols[1]:
            serie_situacao = abono.qtd_servidores_abono_permanencia_por_situacao_servidor()

            fig = px.pie(serie_situacao, values=serie_situacao.values,
                         names=serie_situacao.index, title="Situação dos Servidores com Abono Permanência")
            st.plotly_chart(fig)

        with cols[2]:
            escolaridade = abono.qtd_servidores_abono_permanencia_por_nivel_escolaridade()
            fig = px.pie(escolaridade, values=escolaridade.values,
                         names=escolaridade.index, title="Nível de Escolaridade dos Servidores com Abono Permanência")
            st.plotly_chart(fig)

    elif selected_page == "Dashboard 02":
        st.title("Dashboard 02")

    elif selected_page == "Dashboard 03":
        st.title("Dashboard 03")

    st.write("Abono Permanência")


if __name__ == "__main__":
    main()
