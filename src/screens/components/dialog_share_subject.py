import streamlit as st
import segno
import io

@st.dialog("📚 Share Subject")
def share_subject_dialog(subject_name, subject_code):

    app_domain = "snapclass-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.markdown("""
    <style>

    .share-card{
        background:linear-gradient(135deg,#2563EB,#7C3AED);
        padding:25px;
        border-radius:18px;
        color:white;
        text-align:center;
        margin-bottom:20px;
        box-shadow:0 8px 20px rgba(0,0,0,.15);
    }

    .share-card h2{
        margin:0;
        font-size:30px;
    }

    .share-card p{
        margin-top:8px;
        font-size:16px;
        opacity:.95;
    }

    .info-box{
        background:#F8FAFC;
        padding:18px;
        border-radius:14px;
        border:1px solid #E2E8F0;
        margin-bottom:15px;
    }

    .code-title{
        color:#555;
        font-size:15px;
        font-weight:600;
        margin-bottom:5px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="share-card">
        <h2>📚 {subject_name}</h2>
        <p>Invite students using QR Code or Join Code</p>
    </div>
    """, unsafe_allow_html=True)

    qr = segno.make(join_url)

    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=2)

    left, right = st.columns([1.2,1])

    with left:

        st.markdown("### 🔗 Join Link")

        st.code(join_url)

        st.caption("Students can open this link directly.")

        st.markdown("### 🔑 Join Code")

        st.code(subject_code)

        st.info(
            "Share the Join Link or Join Code with your students using WhatsApp, Email or Classroom."
        )

        if st.button("📋 Copy Join Code", use_container_width=True):
            st.toast("Copy the code manually from above.", icon="📋")

    with right:

        st.markdown("### 📱 QR Code")

        st.image(
            out.getvalue(),
            use_container_width=True
        )

        st.success(
            "Students can simply scan this QR code to join the class."
        )

    st.divider()

    c1,c2 = st.columns(2)

    with c1:
        st.metric("Subject", subject_name)

    with c2:
        st.metric("Join Code", subject_code)

    st.success("✅ Class invitation is ready to share.")