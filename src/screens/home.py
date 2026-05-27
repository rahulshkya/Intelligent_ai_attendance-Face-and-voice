import streamlit as st
from src.screens.ui.base_layout import style_background_home
from src.screens.components.header import header_home
from src.screens.ui.base_layout import style_base_layout
from src.screens.components.footer import footer_home

def home_screen():
     
    header_home()
    style_background_home()
    style_base_layout()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div style='text-align:center;'><h2>I am a Student</h2></div>""", unsafe_allow_html=True)

        st.image(
            "https://imgs.search.brave.com/X4fMWCvjsidg8RkEioFQFRgxtIsRxKaGUqUmhT3lQYk/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3N5c3RlbS9y/ZXNvdXJjZXMvdGh1/bWJuYWlscy8wNDEv/MDQxLzA1NS9zbWFs/bC9zdHVkZW50LWxv/Z28taWNvbi1icmFu/ZC1pZGVudGl0eS1z/aWduLXN5bWJvbC10/ZW1wbGF0ZS12ZWN0/b3IuanBn",
            width=250
        )

        if st.button('Login as Student', use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()
    with col2:
        st.markdown("""<div style='text-align:center;'><h2>I am a Teacher</h2></div>""", unsafe_allow_html=True)

        st.image(
            "https://imgs.search.brave.com/EiiLV-gwZnr94kGhtwV9fKXdu2F-6MEodsckNCTRP1M/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9keW5h/bWljLmJyYW5kY3Jv/d2QuY29tL2Fzc2V0/L2xvZ28vOGJhNTZj/MmMtNjc0YS00NjI5/LWFhMTAtZWU5Njky/YzlhMGMxL2xvZ28t/c2VhcmNoLWdyaWQt/Mng_bG9nb1RlbXBs/YXRlVmVyc2lvbj0x/JnY9NjM4OTk2MzQ0/NzQ0NjMwMDAwJmxh/eW91dD1hdXRvLTEt/MQ",
            width=250
        )

        if st.button('Login as Teacher', use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    footer_home()
