import streamlit as st

def style_background_home():
    st.markdown(
        """        <style>
        .stApp {
            background-color: #5865F2 !important;
        </style>
        """,
        unsafe_allow_html=True
    )

def style_background_dashboard():
    st.markdown(
        """        <style>
        .stApp {
            background-color: #E0E3FF !important;
        </style>
        """,
        unsafe_allow_html=True
    )

def style_base_layout():
    st.markdown(
        """        <style>
        @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
        #MainMenu,footer,header{
          visibility:hidden;
        }
        .block-container{
        padding-top: 0rem;
        padding-bottom: 0rem;}
        </style>
        """,
        unsafe_allow_html=True
    )
