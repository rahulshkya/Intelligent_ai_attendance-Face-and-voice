import time

import streamlit as st

from src.screens.pipelines.face_pipeline import (
    get_face_embeddings,
    train_classifier,
    predict_attendance
)
from src.screens.pipelines.voice_pipeline import get_voice_embedding
from src.screens.ui.base_layout import style_background_dashboard, style_base_layout

from src.screens.components.header import header_home,student_dashboard_header
from src.screens.components.footer import footer_dashboard
from src.screens.components.enroll_dialog import enroll_dialogs
from PIL import Image
import numpy as np

from database.db import get_student_by_id,create_student,get_student_subjects,get_student_attendence


def student_dashboard():
    student_data =st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2=st.column(2,vertical_alignment='center',gap='xxlarge')

    with c1:
        student_dashboard_header()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']}""")
        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data
            st.rerun()

    st.space()
    c1,c2=st.column(2)
    with c1:
        st.header('your Enrolled subjects')
    with c2:
        if st.button('Enroll in subject',type='primary',width='stretch'):
            enroll_dialogs()


    st.divider()

    with st.spinner("Loading your subject..."):
        subjects=get_student_subjects()
        logs=get_student_attendence(student_id)


    stats_map=[]

    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()
    
    if st.session_state.get("is_logged_in") and "student_data" in st.session_state:
        student_dashboard()
        footer_dashboard()
        return
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_home()

    with c2:
        if st.button(
            "Go back to Home",
            type='secondary',
            key='loginbackbtn',
            shortcut="control+backspace"
        ):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID')
    st.write("")
    st.write("")
    
    show_registration = False
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = Image.open(photo_source).convert("RGB")
        img = np.array(img)
        st.image(img)

        with st.spinner("AI is scanning....."):
            st.write("Photo received")
            
            print("Before predict_attendance")

            detected, all_ids, num_faces = predict_attendance(img)

            print("After predict_attendance")
    
            if num_faces == 0:
                st.warning('No face detected. Please try again.')

            elif num_faces > 1:
                st.warning('Multiple faces detected. Please ensure only one face is visible.')

            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    # get_student_by_id may return a dict or a list depending on db implementation
                    all_students = get_student_by_id(student_id)
                    
                   
                    student = None

                    if isinstance(all_students, list):
                        for s in all_students:
                            if str(s.get('id') or s.get('student_id')) == str(student_id):
                                student = s
                                break

                    elif isinstance(all_students, dict):
                        # single student dict
                        if str(all_students.get('id') or all_students.get('student_id')) == str(student_id):
                            student = all_students

                    if student:
                        st.session_state['is_logged_in'] = True
                        st.session_state['user_role'] = 'student'
                        st.session_state['student_data'] = student
                        st.toast(f"Welcome {student.get('name','Student')}! You have successfully logged in.", icon="✅")
                        time.sleep(2)
                        st.rerun()
                else:
                        st.warning('Face recognized, but student not found.')
                        show_registration = True
    

    if show_registration:
    
        with st.container():
            st.header("Student Registration")
            st.write("Please fill in the details below to register.")
            student_name = st.text_input("Enter your name:")
           

            st.subheader('Optional : Voice Enrollment')
            st.info("You can also enroll your voice for future logins. Please record a short audio clip (5-10 seconds) of yourself saying your name.")
            
            audio_data = None
            try:
                audio_data=st.audio_input("Record your voice here:")

            except Exception as e:
                st.error(f"Error occurred while recording audio: {e}")
            
            if st.button('Create_account', type='primary'):
                if student_name:
                    with st.spinner('Creating profile.....'):
                        img = Image.open(photo_source).convert("RGB")
                        img = np.array(img)
                        encodings = get_face_embeddings(img)

                        if len(encodings) == 0:
                            st.error("No face detected.")
                            return
                        else:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                try:
                                    audio_bytes = audio_data.read()
                                    voice_emb = get_voice_embedding(audio_bytes)
                                except Exception:
                                    voice_emb = None

                            response_data = create_student(student_name, face_embedding=face_emb, voice_embedding=voice_emb)
                            print(response_data)

                            if response_data:
                                train_classifier()
                                st.toast(f"Welcome {student_name}! Your profile has been created successfully.", icon="✅")
                                st.session_state['is_logged_in'] = True
                                st.session_state['user_role'] = 'student'
                                st.session_state['student_data'] = response_data

                                time.sleep(2)
                                st.rerun()
                            
                            else:
                                st.error("Failed to create profile. Please try again.")
                else:
                    st.error("Please fill in all fields before registering.")

    footer_dashboard()