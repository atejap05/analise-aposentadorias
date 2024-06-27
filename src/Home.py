import streamlit as st
import os

st.set_page_config(page_title="Home Page",
                   page_icon="🏨", layout="wide")


def main():
    st.title("Home Page")


if __name__ == "__main__":
    main()
    st.session_state['home'] = os.getcwd()
