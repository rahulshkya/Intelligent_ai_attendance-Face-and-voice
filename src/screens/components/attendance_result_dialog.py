import streamlit as st
from database.db import enroll_student_to_subject
from database.config import supabase
from database.db import create_attendance



def show_attendance_results(df,logs):

        st.write("Attendance Result")
        st.dataframe(df,hide_index=True,width="stretch")
        col1,col2=st.columns(2)
        with col1:
            if st.button('Discard',width='stretch'):
                st.toast("Attendance discarded")
                st.session_state.attendance_images=[]
                st.session_state.voice_attendance_results=None
                st.rerun()

        with col2:
            if st.button("confirm and save" ,width='stretch',type="primary"):
                try:
                    create_attendance(logs)
                    st.toast("Attendance taken")
                    st.session_state.attendance_images=[]
                    st.session_state.voice_attendance_results=None
                    st.rerun()

                except Exception as e:
                    st.toast("Error saving attendance")
                    st.error(e)
@st.dialog('attendance result')
def attendance_result_dialog(attendance_df, attendance_to_log):

    show_attendance_results(attendance_df, attendance_to_log)