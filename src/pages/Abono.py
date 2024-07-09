from styles.styles import STYLES
from Analise.abono import Abono
import plotly.express as px
from streamlit_option_menu import option_menu
import streamlit as st
import os
from datetime import datetime
from st_aggrid import AgGrid
import locale

# Configuração de locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Config
st.set_page_config(page_title="Abono Permanência",
                   page_icon="🕗", layout="wide")

# Custom CSS
st.markdown(STYLES.get("METRIC_CARD"), unsafe_allow_html=True)
st.markdown(STYLES.get("BUTTON_BUSCAR"), unsafe_allow_html=True)


def set_menu():
    """
    Função para configurar a sidebar

    """
    with st.sidebar:
        st.title("Menu Abono Permanência")

        selected_page = option_menu(
            menu_title=None,
            options=["Por período", "Por servidor", "Dashboard 03"],
            icons=["receipt-cutoff", "graph-up-arrow", "bar-chart"],
            orientation="vertical",
        )

    return selected_page


def show_dashboard_por_periodo(abono) -> None:
    st.title("Análise anual do abono permanência")
    st.write("Selecione o ano e o mês que deseja consultar.")

    _, col2, col3, _ = st.columns(4)

    anos = abono.get_anos()
    ano = col2.selectbox(label="Ano", options=anos,
                         placeholder="Ano", index=len(anos)-1)

    meses = abono.get_meses(ano)
    mes: int = col3.selectbox("Mês", abono.get_meses(
        ano), index=len(meses)-1, placeholder="Mês")

    if ano and mes:
        # TODO: implementar logica de delta
        data = abono.qtd_servidores_abono_permanencia_por_ano_mes(
            ano, mes)

        # TODO: exportar para aqruivo de renderização das colunas
        cols_card_mes = st.columns(3)
        with cols_card_mes[0]:
            st.write("Mes anterior")
            st.metric(label=data.get("mes_anterior").get("label"),
                      value=data.get("mes_anterior").get("value"))
        with cols_card_mes[1]:
            st.write("Mes atual")
            st.metric(label=data.get("mes_atual").get("label"),
                      value=data.get("mes_atual").get("value"))
        with cols_card_mes[2]:
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

    st.markdown("---")

    # grafico barras qtd serv por unidade
    qtd_por_unidade = abono.qtd_servidores_abono_permanencia_por_unidade_por_ano_mes(
        ano, mes)
    fig = px.bar(qtd_por_unidade, x=qtd_por_unidade.index, y=qtd_por_unidade.values,
                 title=f"Qtd de servidores com abono permanência por Unidade - {mes}/{ano}")
    st.plotly_chart(fig)

    st.markdown("---")

    # montante pago total ano a ano
    montante = abono.montante_pago_abono_permanencia()
    fig_line = px.line(montante, x=montante.index, y=montante.values,
                       title="Montante pago de abono permanência por ano")
    st.plotly_chart(fig_line)


def show_dashboard_por_servidor(abono) -> None:
    # Dashboar para análise por servidor
    # O usuario entra com o nome do servidor e o sistema retorna as informações
    # de abono permanência
    cols_title = st.columns(3)

    with cols_title[1]:
        st.header("Abono por servidor")
        st.markdown(
            "Informe o Nome e CPF para buscar as informações.")

    # TODO: Criar funções ou metodos que retornem esses espacos em branco como margins!
    st.markdown(" ")
    st.markdown(" ")

    input_cols = st.columns(4)
    with input_cols[1]:
        name = st.text_input(
            "Digite o nome do servidor",
            key="input_name",
            placeholder="Nome",
        )

    with input_cols[2]:
        cpf = st.text_input("Digite o CPF do servidor",
                            key="input_cpf",
                            placeholder="CPF",
                            disabled=True if not name else False)

    with input_cols[3]:
        buscar = st.button("Buscar")
    # # TODO:  TESTE --> ALNEY - 00047938700

    def format_brazilian(value):
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    if buscar:

        if name and cpf:
            data = abono.get_servidor_info(name, cpf)
            df_servidor = data.get("df_servidor")

            if not df_servidor.empty:
                nome_servidor = data.get("nome")
                tempo_em_abono = data.get("tempo_em_abono")
                total = data.get("total")

                # TODO: Implementar card com informações gerais do servidor
                cols_name = st.columns(3)
                with cols_name[1]:
                    st.subheader(nome_servidor)

                cols_info_servidor = st.columns(4)
                with cols_info_servidor[1]:
                    anos = tempo_em_abono // 12
                    meses = tempo_em_abono % 12
                    tempo_em_abono_str = f"{anos} anos e {meses} meses"
                    st.metric(label="Tempo em abono",
                              value=tempo_em_abono_str)
                with cols_info_servidor[2]:
                    st.metric(label="Total pago",
                              value=f"R$ {format_brazilian(total)}")

                st.markdown("---")

                # tabela geral de dados
                AgGrid(df_servidor)

                # montatne pago abono permanencia ano a ano barras
                montante_pago = data.get("montante_pago")

                fig = px.bar(montante_pago, x=montante_pago.index, y=montante_pago.values,
                             color=montante_pago.index,
                             text=[f"R$ {format_brazilian(value)}"
                                   for value in montante_pago.values],
                             #  text_auto=True,
                             title=f"Montante pago de abono permanência por ano para o servidor {nome_servidor.lower()}")

                st.plotly_chart(fig)

            else:
                st.write("Nenhum registro encontrado para o servidor informado.")
        else:
            st.error(
                "Informe o nome e o CPF do servidor para buscar as informações.")


def show_dashboard_03() -> None:
    st.title("Dashboard 03")
    st.write("Em construção")


def main() -> None:
    """
    Função principal para execução do script
    """

    pages = {
        "Por período": show_dashboard_por_periodo,
        "Por servidor": show_dashboard_por_servidor,
        "Dashboard 03": show_dashboard_03
    }

    selected_page = set_menu()

    home = os.getcwd(
    ) if 'home' not in st.session_state else st.session_state['home']

    abono = Abono(os.path.join(home, "src\\data\\geral.csv"))
    abono.load_data()

    if selected_page:
        pages[selected_page](abono)


if __name__ == "__main__":
    main()
