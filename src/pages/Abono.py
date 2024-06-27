import os
from datetime import datetime

import streamlit as st
from streamlit_option_menu import option_menu

import plotly.express as px
from Analise.abono import Abono


# Config
st.set_page_config(page_title="Abono Permanência",
                   page_icon="🕗", layout="wide")


st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: rgba(28, 131, 225, 0.1); /* Cor de fundo */
        border: 1px solid rgba(28, 131, 225, 0.1); /* Borda */
        padding: 5% 5% 5% 10%; /* Preenchimento */
        border-radius: 5px; /* Bordas arredondadas */
        color: rgb(30, 103, 119); /* Cor do texto */
        overflow-wrap: break-word;
    }

    </style>
""", unsafe_allow_html=True)


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

    ano_anterior = st.session_state['ano'] if 'ano' in st.session_state else None
    mes_anterior = st.session_state['mes'] if 'mes' in st.session_state else None

    anos = abono.get_anos()
    ano = col2.selectbox(label="Ano", options=anos,
                         placeholder="Ano", index=len(anos)-1)

    meses = abono.get_meses(ano)
    mes: int = col3.selectbox("Mês", abono.get_meses(
        ano), index=len(meses)-1, placeholder="Mês")

    if ano and mes:

        # delta = 0
        # valor_anterior = 0
        # valor_atual = abono.qtd_servidores_abono_permanencia_por_ano_mes(
        #     ano, mes)

        # if ano != ano_anterior or mes != mes_anterior and ano_anterior and mes_anterior:
        #     valor_anterior = abono.qtd_servidores_abono_permanencia_por_ano_mes(
        #         ano_anterior, mes_anterior)
        #     if valor_anterior:
        #         delta = ((valor_atual / valor_anterior) - 1) * 100
        #         delta = f"{round(delta, 2)}%".replace(".", ",")

        # cols = st.columns(3)

        # with cols[0]:
        #     if ano_anterior and mes_anterior:
        #         st.metric(label=f"Servidores com abono permanência em {str(mes_anterior).zfill(2)}/{ano_anterior}",
        #                   value=valor_anterior)

        # with cols[1]:
        #     st.metric(label=f"Servidores com abono permanência em {str(mes).zfill(2)}/{ano}",
        #               value=valor_atual, delta=delta)

        # with cols[2]:

        #     now = datetime.now()
        #     ano_atual = now.year

        #     ultimo_mes = abono.get_meses(ano_atual)[-1]

        #     st.metric(label=f"Servidores com abono permanência em {ultimo_mes}/{ano_atual}",
        #               value=abono.qtd_servidores_abono_permanencia_por_ano_mes(ano_atual, ultimo_mes))

        # if ano != ano_anterior or mes != mes_anterior:
        #     st.session_state['ano'] = ano
        #     st.session_state['mes'] = mes

        ###########################################################################################

        # TODO: Separar para outro modulo a logica para renderizacao dos cards
        # TODO: Adicionar a logica para o delta (variacao percentual mes anterior e proximo mes em relacao ao mes atual)

        qtd_serv_mes_atual = abono.qtd_servidores_abono_permanencia_por_ano_mes(
            ano, mes)
        label_mes_anterior = None
        label_proximo_mes = None

        if ano == 2017 and mes == 1:
            qtd_serv_mes_anterior = 0
            label_mes_anterior = "Sem dados"

        else:

            if mes == 1:
                qtd_serv_mes_anterior = abono.qtd_servidores_abono_permanencia_por_ano_mes(
                    ano - 1, 12)
                label_mes_anterior = f"Servidores com abono permanência em 12/{ano - 1}"

            else:
                qtd_serv_mes_anterior = abono.qtd_servidores_abono_permanencia_por_ano_mes(
                    ano, max(mes - 1, 1))
                label_mes_anterior = f"Servidores com abono permanência em {str(max(mes - 1, 1)).zfill(2)}/{ano if mes != 1 else ano - 1}"

        if ano == 2024 and mes == 5:
            qtd_serv_proximo_mes = 0
            label_proximo_mes = "Sem dados"

        else:

            if mes == 12:
                qtd_serv_proximo_mes = abono.qtd_servidores_abono_permanencia_por_ano_mes(
                    ano + 1, 1)
                label_proximo_mes = f"Servidores com abono permanência em 01/{ano + 1}"

            else:
                qtd_serv_proximo_mes = abono.qtd_servidores_abono_permanencia_por_ano_mes(
                    ano, min(mes + 1, 12))
                label_proximo_mes = f"Servidores com abono permanência em {str(min(mes + 1, 12)).zfill(2)}/{ano + 1 }"

        cols = st.columns(3)
        with cols[0]:
            st.write("Mes anterior")
            st.metric(label=label_mes_anterior,
                      value=qtd_serv_mes_anterior)
        with cols[1]:
            st.write("Mes atual")
            st.metric(label=f"Servidores com abono permanência em {str(mes).zfill(2)}/{ano}",
                      value=qtd_serv_mes_atual)
        with cols[2]:
            st.write("Mes seguinte")
            st.metric(label=label_proximo_mes,
                      value=qtd_serv_proximo_mes)

    st.markdown("---")

    # TODO: sessao para analise comparativa entre os anos
    st.write("adicionar DateTimePicker para selecionar o intervalo de datas")


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
