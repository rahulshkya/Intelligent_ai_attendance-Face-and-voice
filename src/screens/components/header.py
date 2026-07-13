import streamlit as st
from textwrap import dedent

def header_home():

    logo_url ="https://imgs.search.brave.com/4lmjV8ZZABRoYJpmWilJVMjTXIQACFR-fyrdUuQ3Yxk/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTIw/MjU1ODMyNS92ZWN0/b3IvZ3JhZHVhdGUt/cHJvZ3JhbS1ncmFk/aWVudC1jb2xvci1w/YXBlci1jdXQtc3R5/bGUtaWNvbi1kZXNp/Z24uanBnP3M9NjEy/eDYxMiZ3PTAmaz0y/MCZjPTlxQ3lmazNk/ZXdTVG91Zm9ORS1Y/ZUs0RWZMUmVoMFpP/WTBfU3hzQUxpVkk9"

    st.markdown(
        f"""
        <div style="text-align:center;display:flex;flex-direction:column;align-items:center;"> 
            <img src="{logo_url}" 
                 style="width:100px;height:100px;margin-bottom:1rem;margin-top:1rem;border-radius:50%;">
            <h1 style="color:white; text-align:center;">SNAP <br>CLASS</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


from datetime import datetime


def student_dashboard_header():

    student = st.session_state["student_data"]

    today = datetime.now().strftime("%d %B %Y")
    current_time = datetime.now().strftime("%I:%M %p")

    st.markdown(f"""
    <style>

    .dashboard-header{{
        background:linear-gradient(135deg,#2563EB,#7C3AED);
        border-radius:22px;
        padding:32px;
        color:white;
        box-shadow:0 12px 35px rgba(0,0,0,.22);
        margin-bottom:25px;
    }}

    .brand{{
        font-size:36px;
        font-weight:800;
        letter-spacing:1px;
    }}

    .subtitle{{
        font-size:17px;
        opacity:.9;
        margin-top:4px;
    }}

    .welcome{{
        font-size:30px;
        font-weight:700;
        margin-top:25px;
    }}

    .status{{
        display:inline-block;
        margin-top:12px;
        background:rgba(255,255,255,.18);
        padding:8px 18px;
        border-radius:30px;
        font-weight:600;
    }}

    .metric-card{{
    background:white;
    border-radius:18px;
    padding:20px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,0,0,.08);

    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;

    min-height:140px;
}}
    .metric-title{{
        color:#777;
        font-size:15px;
    }}

    .metric-value{{
        color:#2563EB;
        font-size:24px;
        font-weight:bold;
        margin-top:8px;
        word-break: keep-all;
    }}

    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(dedent(f"""
    <div class="dashboard-header">

    <div class="brand">
            🎓 SnapClass
    </div>

    <div class="subtitle">
            Intelligent AI Attendance System
    </div>

    <div class="welcome">
            👋 Welcome, {student["name"]}
    </div>

    <div class="status">
            🟢 Face Authentication Successful
    </div>

    </div>
    """), unsafe_allow_html=True)

    c1,c2=st.columns(2)

    with c1:
        st.markdown(dedent(f"""
        <div class="metric-card">
        <div class="metric-title">
            🆔 Student ID
        </div>

        <div class="metric-value">
            {student["student_id"]}
        </div>

        </div>
        """),unsafe_allow_html=True)

    with c2:
        st.markdown(dedent(f"""
        <div class="metric-card">
        <div class="metric-title">
            📅 Date
        </div>

        <div class="metric-value">
            {today}
        </div>

        </div>
        """),unsafe_allow_html=True)
    
    c3,c4=st.columns(2)
    with c3:
        st.markdown(dedent(f"""
        <div class="metric-card">
        <div class="metric-title">
            ⏰ Login Time
        </div>

        <div class="metric-value">
            {current_time}
        </div>

        </div>
        """),unsafe_allow_html=True)

    with c4:
        st.markdown(dedent("""
        <div class="metric-card">

        <div class="metric-title">
            📷 Status
        </div>

        <div class="metric-value" style="color:green;">
            VERIFIED
        </div>

        </div>
        """),unsafe_allow_html=True)
   

