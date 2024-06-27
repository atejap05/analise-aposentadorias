import streamlit as st
from st_aggrid import AgGrid
import plotly.express as px
from Analise.abono import Abono


st.set_page_config(page_title="Home Page",
                   page_icon="🏨", layout="wide")

uploaded_file = st.sidebar.file_uploader("Choose a file", type="xlsx")

if uploaded_file is not None:
    abono = Abono(uploaded_file)
    abono.load_data()

    st.session_state["abono"] = abono


def main():

    st.title("Home Page")


if __name__ == "__main__":
    main()
