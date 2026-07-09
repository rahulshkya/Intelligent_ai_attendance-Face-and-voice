import streamlit as st
from src.screens.components.header import header_home
from src.screens.components.footer import footer_home
from src.screens.ui.base_layout import style_base_layout, style_background_dashboard
from src.screens.components.footer import footer_dashboard
from database.config import supabase
from database.db import check_teacher_exists, create_teacher, teacher_login,get_teacher_subject
from src.screens.components.dialog_create_subjects import create_subject_dialog
from src.screens.components.subject_card import subject_card
from src.screens.components.dialog_share_subject import share_subject_dialog

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


import streamlit as str


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

    # Info Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="title">Teacher ID</div>
            <div class="value">
                {teacher.get("teacher_id") or teacher.get("id")}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <div class="title">Today's Classes</div>
            <div class="value">3</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
            <div class="title">Students</div>
            <div class="value">120</div>
        </div>
        """, unsafe_allow_html=True)

    
    st.divider()

    st.write("")
    st.write("")

    main4, main5 = st.columns(2)

    with main4:
        if st.button("📊 Attendance Reports", use_container_width=True):
            st.session_state.current_teacher_tab = "reports"

    with main5:
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
    st.header('Take ai attendace')
    
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
    st.header('Take ai attendace reports')

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
    footer_dashboard()
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