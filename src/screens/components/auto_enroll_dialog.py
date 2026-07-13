import streamlit as st
from database.db import enroll_student_to_subject
from database.config import supabase

import time

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id=st.session_state.student_data['student_id']

    res =supabase.table('subjects').select('subject_id,name').eq('subject_code',subject_code).execute()
    if not res.data:
        st.error("subject code not found!")
        if st.button("close"):
            st.query_params.clear()
            st.rerun()
        return 
    subject=res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        st.warning("You are already enrolled in this subject!")
        if st.button("close"):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"## Do you want to enroll in **{subject['name']}** ?")
    col1,col2=st.columns(2)
    
    with col1:
        if st.button(' No Thanks !'):
            st.query_params.clear()
            st.rerun()
       
    
    with col2:
        if st.button("Enroll Now",type='primary',width='stretch',args=(student_id,subject['subject_id'],)):
            enroll_student_to_subject(student_id,subject['subject_id'])
            st.success("You have been successfully enrolled in this subject!")
            st.query_params.clear()
            time.sleep(1)
            st.rerun()
            

