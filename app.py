import streamlit as st

import src.screens.home as home
from src.screens.student import student_screen
from src.screens import teacher

from src.screens.components.auto_enroll_dialog import auto_enroll_dialog


def main():

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:

        case "student":
            student_screen()

        case "teacher":
            teacher.main()

        case _:
            home.home_screen()

    join_code = st.query_params.get('join-code')

    if join_code:

        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()

        if (
            st.session_state.get('is_logged_in')
            and st.session_state.get('user_role') == 'student'
        ):
            auto_enroll_dialog(join_code)


if __name__ == "__main__":
    main()