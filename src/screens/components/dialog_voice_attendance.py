import streamlit as st
import supabase
from database.config import supabase
from src.screens.components.attendance_result_dialog import show_attendance_results
from src.screens.pipelines.voice_pipeline import process_bulk_audio
from datetime import datetime
import pandas as pd

@st.dialog("Voice Attendance")
def Voice_attendance_dialog(selected_subject_id):
    st.write("Record your voice for attendance")
    audio_data=None
    audio_data = st.audio_input("Record your voice", sample_rate=16000)

    if st.button("analyze", type="primary", width="stretch"):
        with st.spinner("Processing audio...."):
            enrolled_res=supabase.table('subject_students').select("*,students(*)").eq("subject_id",selected_subject_id).execute()
            enrolled_students=enrolled_res.data

            if not enrolled_students:
                    st.warning("No students enrolled in this subject.")
                    return
            candidates_dict = {}

            for s in enrolled_students:
                if s["students"].get("voice_embedding"):
                    candidates_dict[
                        s["students"]["student_id"]
                    ] = s["students"]["voice_embedding"]

            if not candidates_dict:
                st.warning("No students with voice embeddings found.")
                return

            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)
            results,attendance_to_log=[],[]

            current_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for node in enrolled_students:
                student=node['students']
                score=detected_scores.get(student['student_id'],0.0)
                is_present = score >= 0.65

                results.append({
                    "name":student['name'],
                    "id":student['student_id'],
                    "Source": f"Voice ({score:.2f})" if is_present else "_",
                    "status":"Present" if is_present else "Absent"

                })
                attendance_to_log.append(
                    {
                        'student_id':student['student_id'],
                        'subject_id':selected_subject_id,
                        'timestamp':current_timestamp,
                        'is_present':bool(score)                                                          
                    }
                )
            st.session_state.voice_attendance_results=(pd.DataFrame(results),attendance_to_log)
    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results,logs=st.session_state.voice_attendance_results
        show_attendance_results(df_results,logs)
