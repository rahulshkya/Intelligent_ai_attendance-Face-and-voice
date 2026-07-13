import streamlit as st
from src.screens.components.header import header_home
from src.screens.ui.base_layout import (
    style_background_home,
    style_base_layout
)


def home_screen():
    
    style_background_home()
    style_base_layout()

    st.markdown("""
    <style>

    .hero{
        text-align:center;
        padding:20px;
    }

    .hero h1{
        font-size:60px;
        color:white;
        margin-bottom:5px;
        font-weight:800;
    }

    .hero p{
        color:white;
        font-size:20px;
        opacity:0.9;
    }

    .card{
        background:white;
        padding:25px;
        border-radius:22px;
        text-align:center;
        box-shadow:0px 8px 25px rgba(0,0,0,.18);
        transition:.3s;
        height:520px;
    }

    .card:hover{
        transform:translateY(-8px);
        box-shadow:0px 12px 35px rgba(0,0,0,.25);
    }

    .title{
        font-size:34px;
        font-weight:bold;
        color:#2c3e50;
        margin-top:15px;
    }

    .desc{
        color:#241f3a;
        font-size:18px;
        margin-top:10px;
    }

    .feature{
        background:white;
        border-radius:18px;
        padding:20px;
        text-align:center;
        box-shadow:0px 5px 18px rgba(0,0,0,.12);
    }

    .feature h3{
        color:#5B5FEF;
    }
    .st-key-student_card,
    .st-key-teacher_card {
    padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    header_home()

    st.markdown("""
    <div class="hero">
        <p>AI Powered Attendance Management System</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2 = st.columns(2, gap="large")

    left, col1, col2, right = st.columns(
    [2, 3, 3, 2],
    gap="medium")


    with col1:
        with st.container(border=True, key="student_card"):
            st.image("assets/student_logo.png")

            st.markdown("""
            <div class="title">🎓 Student Portal</div>
            <div class="desc">
            Login securely using Face Recognition and Voice Authentication.
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            st.write("")

            if st.button(
                "🚀 Continue as Student",
                width="content",
                
            ):
                st.session_state["login_type"] = "student"
                st.rerun()


    with col2:
        with st.container(border=True, key="teacher_card"):
            st.image("assets/teacher_logo.png")

            st.markdown("""
            <div class="title">👨‍🏫 Teacher Portal</div>
            <div class="desc">
            Manage students, attendance records and classroom activities.
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            st.write("")

            if st.button(
                "🚀 Continue as Teacher",
                width="content",
                
            ):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    st.write("")
    st.write("")
    st.divider()

    st.subheader("✨ Features")

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.markdown("""
        <div class="feature">
            <h3>😊</h3>
            <b>Face Recognition</b>
            <br><br>
            Fast & Accurate Login
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature">
            <h3>🎤</h3>
            <b>Voice Login</b>
            <br><br>
            Optional Voice Authentication
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature">
            <h3>⚡</h3>
            <b>AI Powered</b>
            <br><br>
            Smart Attendance Detection
        </div>
        """, unsafe_allow_html=True)

    with f4:
        st.markdown("""
        <div class="feature">
            <h3>☁️</h3>
            <b>Cloud Database</b>
            <br><br>
            Secure Supabase Storage
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

