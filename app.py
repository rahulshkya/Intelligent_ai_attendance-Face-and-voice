import streamlit as st
import src.screens.home as home
import src.screens.student as student
import src.screens.teacher as teacher
def main():

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
   
    match st.session_state['login_type']:
        case "student":
            student.student_screen()
        case "teacher":
            teacher.main()
        case _:
            home.home_screen()
main()