import os
from datetime import datetime

import streamlit as st
from streamlit_option_menu import option_menu

import plotly.express as px
from Analise.abono import Abono
from styles.styles import STYLES


# Config
st.set_page_config(page_title="Abono Permanência",
                   page_icon="🕗", layout="wide")

# Custom CSS
st.markdown(STYLES.get("METRIC_CARD"), unsafe_allow_html=True)


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


def show_dashboard_01(abono) -> None:
    st.title("Análise anual do abono permanência")
    st.write("Selecione o ano e o mês que deseja consultar.")

    col1, col2, col3, col4 = st.columns(4)

    anos = abono.get_anos()
    ano = col2.selectbox(label="Ano", options=anos,
                         placeholder="Ano", index=len(anos)-1)

    meses = abono.get_meses(ano)
    mes: int = col3.selectbox("Mês", abono.get_meses(
        ano), index=len(meses)-1, placeholder="Mês")

    if ano and mes:
        data = abono.qtd_servidores_abono_permanencia_por_ano_mes(
            ano, mes)

        # TODO: exportar para aqruivo de renderização das colunas
        colsCardMes = st.columns(3)
        with colsCardMes[0]:
            st.write("Mes anterior")
            st.metric(label=data.get("mes_anterior").get("label"),
                      value=data.get("mes_anterior").get("value"))
        with colsCardMes[1]:
            st.write("Mes atual")
            st.metric(label=data.get("mes_atual").get("label"),
                      value=data.get("mes_atual").get("value"))
        with colsCardMes[2]:
            st.write("Mes seguinte")
            st.metric(label=data.get("mes_proximo").get("label"),
                      value=data.get("mes_proximo").get("value"))

    st.markdown("---")

    # graico de barras qtd por uf ano mes
    qtd_por_uf_res = abono.qtd_servidores_abono_permanencia_por_uf_residencia_por_ano_mes(
        ano, mes)
    fig = px.bar(qtd_por_uf_res, x=qtd_por_uf_res.index, y=qtd_por_uf_res.values,
                 title=f"Qtd de servidores com abono permanência por UF - {mes}/{ano}")
    st.plotly_chart(fig)


def main() -> None:
    """
    Função principal para execução do script
    """

    pages = {
        "Dashboard 01": show_dashboard_01,
        "Dashboard 02": None,
        "Dashboard 03": None
    }

    selected_page = set_menu()

    home = os.getcwd(
    ) if 'home' not in st.session_state else st.session_state['home']

    abono = Abono(os.path.join(home, "src\\data\\geral.csv"))
    abono.load_data()

    # Seleção dinâmica da página
    pages.get(selected_page, None)(abono) if pages.get(
        selected_page, None) else st.title("Página em construção")


if __name__ == "__main__":
    main()
