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
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
        #MainMenu,footer,header{
          visibility:hidden;
        }
        .block-container{
        padding-top: 0rem;
        padding-bottom: 0rem;}
        h1{
        font-family:'Climate Crisis', sans-serif !important;
        font-size: 3rem !important;
        line-height:1.1 !important;
        margin-bottom: 0rem !important;

        }

        h2{
        font-family:'Climate Crisis', sans-serif !important;
        font-size: 2.5rem !important;
        line-height:1.1 !important;
        margin-bottom: 0rem !important;

        }
        h3,h4,h5,p{
        font-family:'Outfit', sans-serif !important;
        }
        button[kind="primary"]{
        background: #5865F2 !important;
        color: white !important;
        border-radius:1.5rem !important;
        border: none !important;
        transition: transform 0.3s ease-in-out !important;}

        button[kind="secondary"]{
        background: #EB459E !important;
        color: white !important;
        border-radius:1.5rem !important;
        border: none !important;
        transition: transform 0.3s ease-in-out !important;}

        button[kind="tertiary"]{
        background: black !important;
        color: white !important;
        border-radius:1.5rem !important;
        border: none !important;
        transition: transform 0.3s ease-in-out !important;}

        .stButton>button{
            background:linear-gradient(135deg,#5B5FEF,#7C3AED);
            color:white;
            border:none;
            border-radius:12px;
            height:55px;
            font-size:18px;
            font-weight:700;
            transition:.3s;
        }

        .stButton>button:hover{
            transform:scale(1.03);
            background:linear-gradient(135deg,#7C3AED,#5B5FEF);
        }

        button:hover{
        transform: scale(1.05) !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
