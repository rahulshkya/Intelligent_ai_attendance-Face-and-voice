import streamlit as st
from src.screens.components.header import header_home
from src.screens.components.footer import footer_home
from src.screens.ui.base_layout import style_base_layout, style_background_dashboard
from src.screens.components.footer import footer_dashboard

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


def register_teacher(username: str, name: str, password: str, confirm: str):
    if password != confirm:
        st.error('Passwords do not match')
        return False
    if not password:
        st.error('Please enter a password')
        return False

    st.session_state['teacher_username'] = username
    st.session_state['teacher_name'] = name
    st.session_state['teacher_registered_password'] = password
    st.session_state['teacher_authenticated'] = True
    st.success('Registered successfully and logged in')
    return True


def login_teacher(username: str, password: str):
    registered_username = st.session_state.get('teacher_username', '')
    registered_password = st.session_state.get('teacher_registered_password', '')

    if not registered_username or not registered_password:
        st.error('Please register first')
        return False

    if username == registered_username and password == registered_password:
        st.session_state['teacher_authenticated'] = True
        st.success('Login successful')
        return True

    st.error('Username or password does not match registered credentials')
    return False


def main():
    ensure_teacher_state()

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
            st.experimental_rerun()

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

            register = st.form_submit_button('Register Now')

        if register:
            register_teacher(username, name, password, confirm)

    with login_tab:
        with st.form('teacher_login_form'):
            st.write('')
            login_username = st.text_input('Username', value=st.session_state.get('teacher_username', '@abhishek'), key='login_username')
            login_password = st.text_input('Password', type='password', key='login_password')
            login_submit = st.form_submit_button('Login')

        if login_submit:
            login_teacher(login_username, login_password)

    if st.session_state.get('teacher_authenticated'):
        st.info(f"Logged in as {st.session_state.get('teacher_name', 'Teacher')} ({st.session_state.get('teacher_username', '')})")
        if st.button('Logout'):
            st.session_state['teacher_authenticated'] = False
            st.rerun()

    footer_dashboard()


if __name__ == '__main__':
    main()