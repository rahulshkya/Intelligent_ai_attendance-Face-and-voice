
import pandas as pd
import streamlit as st
from datetime import datetime
from src.screens.components.header import header_home

from src.screens.ui.base_layout import style_base_layout, style_background_dashboard
from src.screens.components.footer import footer_dashboard
from database.config import supabase
from database.db import check_teacher_exists, create_teacher, teacher_login,get_teacher_subject
from src.screens.components.dialog_create_subjects import create_subject_dialog
from src.screens.components.subject_card import subject_card
from src.screens.components.dialog_share_subject import share_subject_dialog
from src.screens.components.add_photo_dialog import add_photo_dialog
from src.screens.pipelines.face_pipeline import predict_attendance
from src.screens.components.attendance_result_dialog import attendance_result_dialog
import numpy as np
from database.config import supabase 
from src.screens.components.dialog_voice_attendance import Voice_attendance_dialog
from database.db import get_teacher_subject_for_attendance

 
def ensure_teacher_state():
    if 'teacher_username' not in st.session_state:
        st.session_state['teacher_username'] = '@abhishek'
    if 'teacher_name' not in st.session_state:
        st.session_state['teacher_name'] = 'Abhishek Sharma'
    if 'teacher_password' not in st.session_state:
        st.session_state['teacher_password'] = ''
    if 'teacher_confirm' not in st.session_state:
        st.session_state['teacher_confirm'] = ''
    if 'teacher_registered_password' not in st.session_state:
        st.session_state['teacher_registered_password'] = ''
    if 'teacher_pw_visible' not in st.session_state:
        st.session_state['teacher_pw_visible'] = False
    if 'teacher_authenticated' not in st.session_state:
        st.session_state['teacher_authenticated'] = False


def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
        return False, "All fields are required."
    if check_teacher_exists(teacher_username):
        return False, "Username already exists."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True , "successfully registered"

    except Exception as e:
        return False, f"unexpexting error: {str(e)}"




def teacher_dashboard():

    if "teacher_data" not in st.session_state:
        st.error("Teacher not logged in.")
        return

    teacher = st.session_state["teacher_data"]
    st.markdown("""
    <style>

    .hero{
        background:linear-gradient(135deg,#2563EB,#7C3AED);
        padding:35px;
        border-radius:20px;
        color:white;
        box-shadow:0 10px 25px rgba(0,0,0,.20);
        margin-bottom:25px;
    }

    .hero h1{
        margin:0;
        font-size:40px;
    }

    .hero p{
        margin-top:8px;
        font-size:18px;
        opacity:.9;
    }

    .card{
        background:white;
        padding:25px;
        border-radius:18px;
        text-align:center;
        box-shadow:0 6px 20px rgba(0,0,0,.10);
    }

    .title{
        color:#666;
        font-size:15px;
    }

    .value{
        color:#2563EB;
        font-size:30px;
        font-weight:bold;
        margin-top:10px;
    }

    </style>
    """, unsafe_allow_html=True)

    # Hero Card
    st.markdown(f"""
    <div class="hero">
        <h1>👨‍🏫 Welcome, {teacher.get("name","Teacher")}</h1>
        <p>AI Attendance Management Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

   
    
    st.divider()

    st.write("")
    st.write("")

    

    

    
    if st.button("🚪 Logout", use_container_width=True): 
            st.session_state['is_logged_in'] = False
            if "teacher_data" in st.session_state:
                del st.session_state["teacher_data"]
            st.rerun()

    st.divider()

    st.subheader("⚡ Quick Actions")

    
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    main1, main2, main3 = st.columns(3)
    with main1:
        if st.button("📸 Take Attendance", use_container_width=True):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with main2:
        if st.button("📚 Manage subjects", use_container_width=True):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with main3:
        if st.button("👨‍🎓 View Attendance Records", use_container_width=True):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()
    
    if st.session_state.current_teacher_tab  =='take_attendance':
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == 'manage_subjects':
        manage_subjects_tab()

    if st.session_state.current_teacher_tab  =='attendance_records':
        attendance_reports_tab()
        

    st.subheader("📈 Dashboard Overview")

    left, right = st.columns(2)

    with left:
        st.info("""
### 📅 Today's Schedule

• BCA Semester-I

• AI Lab

• Web Development

• DBMS Practical
""")

    with right:
        st.success("""
### 🤖 System Status

✅ Face Recognition Online

✅ Voice Authentication Ready

✅ Supabase Connected

✅ AI Model Loaded
""")
        
footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id=st.session_state.teacher_data['teacher_id']

    st.header('Take ai attendace')

    if 'attendence_image' not in st.session_state:
        st.session_state['attendence_image'] = []
    
    subjects =get_teacher_subject(teacher_id)

    if not subjects:
        st.warning("No subjects found. Please create a subject first.")
        return
    
    subject_options={f"{s['name']}-{s['subject_code']}":s['subject_id'] for s in subjects}
    col1,col2=st.columns([3,1])
    with col1:
       selected_subject_label= st.selectbox('Select Subject',options=list(subject_options.keys()))

    with col2:
           if st.button('Add Photos',type='primary',width='stretch'):
               
               add_photo_dialog()
    selected_subject_id=subject_options[selected_subject_label]

    st.divider()
    
    if st.session_state.attendence_image:
        st.header('Selected Photos')
        gallery_cols=st.columns(3)
        for idx,img in enumerate(st.session_state.attendence_image):
            with gallery_cols[idx%3]:
                st.image(img, width="stretch")
    c1,c2,c3=st.columns(3)
    has_photos = bool(st.session_state.attendence_image)
    with c1:
        if st.button('Clear Photos',type='tertiary',width='stretch',disabled=not has_photos):
            st.session_state.attendence_image.clear()
            st.rerun()

    with c2:
        
        if st.button('Run face anaylysis',type='primary',width='stretch',disabled=not has_photos):
            with st.spinner("Analyzing photos and marking attendance..."): 
                all_detected_id ={}

                for idx,img in enumerate(st.session_state.attendence_image):
                    img_np=np.array(img)
                    detected,_,_=predict_attendance(img_np)

                    if detected:
                        for sid in detected:
                            student_id =int(sid)
                            all_detected_id.setdefault(student_id,[]).append(f"Photo {idx+1}")

                enrolled_res=supabase.table('subject_students').select("*,students(*)").eq("subject_id",selected_subject_id).execute()
                enrolled_students=enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this subject.")
                    return
                
                else:
                    results,attendance_to_log=[],[]

                    current_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    for node in enrolled_students:
                        student=node['students']
                        sources=all_detected_id.get(int(student['student_id']),[])
                        is_present=len(sources) > 0

                        results.append({
                            "name":student['name'],
                            "id":student['student_id'],
                            "Source":",".join(sources) if is_present else "_",
                            "status":"Present" if is_present else "Absent"

                        })
                        attendance_to_log.append(
                            {
                                'student_id':student['student_id'],
                                'subject_id':selected_subject_id,
                                'timestamp':current_timestamp,
                                'is_present':bool(sources)                                                          
                            }
                        )
            attendance_result_dialog(pd.DataFrame(results),attendance_to_log)


    with c3:
            if st.button('Use voice assistant',type='tertiary',width='stretch'):
                Voice_attendance_dialog(selected_subject_id)
    
def manage_subjects_tab():
    
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1,col2 =st.columns(2)
    with col1:
        st.header('manage subjects')

    with col2:
        if st.button('Create New Subjects',width='stretch'):
            create_subject_dialog(teacher_id)

    #list all subjects
    subjects=get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            print(sub)
            print(sub.keys())
            stats=[
                ('🧑‍🦰','students',sub['Total students']),
                ('⏱️','Classes',sub['total_classes']),
            ]

        def share_btn():
            if st.button(
                f"Share Code : {sub['name']}",
                key=f"share_{sub['subject_code']}",
                icon=":material/share:"
            ):
            
                share_subject_dialog(
                    sub["name"],
                    sub["subject_code"]
                )

            st.space()
        print(type(stats))
        print(stats)
        subject_card(
            name =sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.warning('no subjects found, create one above')


def attendance_reports_tab():
    st.header('Attendance Reports')
    teacher_id = st.session_state.teacher_data['teacher_id']
    records=get_teacher_subject_for_attendance(teacher_id)
    if not records:
        st.warning("No attendance records found.")
        return
    data=[]

    for r in records:
        ts=r.get('timestamp')
        data.append({
            "ts_group":ts.split(" ")[0] if ts else "Unknown",
            "time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "Unknown",
            "Subject": r["subjects"]["name"],
            "Subject_code": r["subjects"]["subject_code"],
            "is_present": bool(r.get('is_present',False))
        })
        
    df=pd.DataFrame(data)
    summary=(
        df.groupby(['ts_group','time','Subject','Subject_code'])
        .agg(
            Present_count=('is_present','sum'),
            Total_count=('is_present','count')
        ).reset_index()
    )
    summary['Attendance Stats']=(
        "✅"+summary['Present_count'].astype(str)+" /" +summary['Total_count'].astype(str)
            )
    display_df=(summary.sort_values (by='ts_group',ascending=False)
                [['time','Subject','Subject_code','Attendance Stats']]
                )
    st.dataframe(display_df,hide_index=True,width="stretch")
     

def login_teacher(username,password):
    if not username or not password:
        return False

    teacher = teacher_login(username,password)

    if teacher:
        st.session_state.teacher_authenticated = True
        st.session_state.teacher_data = teacher

        return True

    return False
 
def main():
    ensure_teacher_state()
    
    if st.session_state.get("teacher_authenticated"):
        teacher_dashboard()
        return
    header_home()
    style_background_dashboard()
    style_base_layout()
    
    # Back button
    cols = st.columns([1, 2, 1])
    with cols[1]:
        if st.button('Go back to Home'):
            st.session_state['login_type'] = None
            st.rerun()

    # Password visibility toggle outside the form (st.button is not allowed inside forms)
    toggle_cols = st.columns([8, 1])
    with toggle_cols[1]:
        if st.button('👁️', key='toggle_teacher_pw'):
            st.session_state['teacher_pw_visible'] = not st.session_state['teacher_pw_visible']
            st.rerun()

    st.markdown("""
    <div style='text-align:center; margin-top:1rem;'>
        <h1 style='color:black; font-weight:800;'>Register or login as teacher</h1>
    </div>
    """, unsafe_allow_html=True)
    footer_dashboard()
    register_tab, login_tab = st.tabs(['Register', 'Login'])

    with register_tab:
        with st.form('teacher_register_form'):
            st.write('')
            username = st.text_input('Enter username', value=st.session_state.get('teacher_username', '@abhishek'), key='register_username')
            name = st.text_input('Enter name', value=st.session_state.get('teacher_name', 'Abhishek Sharma'), key='register_name')

            pw_col, _ = st.columns([8, 1])
            with pw_col:
                pwd_type = 'default' if st.session_state['teacher_pw_visible'] else 'password'
                password = st.text_input('Enter password', type=pwd_type, key='register_password')
                confirm = st.text_input('Confirm password', type=pwd_type, key='register_confirm')
                register_teachers =  st.form_submit_button('Register Now')
                if register_teachers:
                    success,message= register_teacher(username,name,password,confirm)
                    if success:
                        st.success(message)
                        import time
                        time.sleep(2)
                        st.session_state.teacher_login_type="login"
                    else:
                        st.error(message)



       

    with login_tab:
        with st.form('teacher_login_form'):
            st.write('')
            login_username = st.text_input('Username', value=st.session_state.get('teacher_username', '@abhishek'), key='login_username')
            login_password = st.text_input('Password', type='password', key='login_password')
            if st.form_submit_button('Login'):
                teacher = login_teacher(login_username,login_password)
                if teacher:
                    st.toast("welcome back!",icon="✅")
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid username and password combo")
                    
    
       
   
    if st.session_state.get('teacher_authenticated'):
        st.info(f"Logged in as {st.session_state.get('teacher_name', 'Teacher')} ({st.session_state.get('teacher_username', '')})")
        if st.button("Logout"):

            st.session_state.teacher_authenticated = False

            if "teacher_data" in st.session_state:
                del st.session_state["teacher_data"]

            st.rerun()




if __name__ == '__main__':
    main()