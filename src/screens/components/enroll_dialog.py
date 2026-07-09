import streamlit as st
from database.db import enroll_student_to_subject
from database.config import supabase
import time

@st.dialog('enroll and subjects')
def enroll_dialogs():
   st.write("Enter the subject code provided by your teacher to enroll")
   join_code=st.text_input("subject code",placeholder='EG OS433')
   

   if st.button("Enroll Now",type="primary",width="stretch"):
      if join_code:
         res =supabase.table("subjects").select("subject_id,name,subject_code").eq("subject_code",join_code).execute()
         if res.data:
            subject=res.data[0]
            student_id=st.session.student_data['student_id']

            check=supabase.table('subject_students').select("*").eq("subject_id",subject['subject_id']).eq("student_id",student_id).execute()
            if check.data:
                st.warning("you are already enrolled in this program")
            else:
                enroll_student_to_subject(student_id,subject['subject_id'])
                st.success("successfully enrolled !!")
                time.sleep(2)
                st.rerun()

      else:
            st.warning('Plase enter a subject code')


