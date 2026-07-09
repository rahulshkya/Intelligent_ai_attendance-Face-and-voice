import streamlit as st
from database.db import create_subject

@st.dialog('create new subject')
def create_subject_dialog(teacher_id):
    st.write('Enter the details of new subject')
    sub_id=st.text_input('subject code',placeholder='OS104')
    sub_name=st.text_input("subject name",placeholder='Introduction to Operating system')
    sub_section=st.text_input('section',placeholder='A')

    if st.button("Create Subject Now",type='primary',width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("subject Create Succesfully !")
                st.rerun()
            except Exception as e:
                st.error(f'Error : {str(e)}')
        else:
            st.warning('please fill all the fields')