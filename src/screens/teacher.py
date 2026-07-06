import streamlit as st
from src.screens.components.header import header_home
from src.screens.components.footer import footer_home
from src.screens.ui.base_layout import style_base_layout, style_background_dashboard
from src.screens.components.footer import footer_dashboard
from database.config import supabase
from database.db import check_teacher_exists, create_teacher, teacher_login

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
    teacher_data = st.session_state.teacher_data
    st.header(f"""welcome , {teacher_data['name']}""")

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

    footer_dashboard()


if __name__ == '__main__':
    main()