import streamlit as st
from src.screens.ui.base_layout import style_background_home
from src.screens.components.header import header_home
from src.screens.ui.base_layout import style_base_layout
def main():
    st.header('Home Screen')
    
    header_home()
    style_base_layout()
    style_background_home()
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Login as Student'):
            st.session_state['login_type'] = 'student'
            st.rerun()
    with col2:
        if st.button('Login as Teacher'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
main()