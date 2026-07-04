import streamlit as st
from src.screens.components.header import header_home
from src.screens.components.footer import footer_home
from src.screens.ui.base_layout import style_base_layout, style_background_dashboard


def main():
    header_home()
    style_background_dashboard()
    style_base_layout()

    # Top back button
    cols = st.columns([1, 2, 1])
    with cols[1]:
        if st.button('Go back to Home'):
            st.session_state['login_type'] = None
            st.rerun()

    # Page title
    st.markdown(
        """
        <div style='text-align:center; margin-top:1rem;'>
            <h1 style='color:black; font-weight:800;'>Login with FaceID</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Custom styles for cards and buttons
    st.markdown(
        """
        <style>
        .card {
            background: white;
            border-radius: 16px;
            padding: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
        .camera-frame{
            width:100%;
            height:360px;
            object-fit:cover;
            border-radius:12px;
        }
        .take-btn{
            background:#5865F2;
            color:white;
            padding:12px 22px;
            border-radius:999px;
            display:inline-block;
            font-weight:700;
        }
        .small-preview{
            width:160px;
            height:160px;
            border-radius:16px;
            object-fit:cover;
            box-shadow:0 8px 20px rgba(0,0,0,0.12);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main columns: camera and small preview (live capture)
    left, right = st.columns([3, 1])
    with left:
        st.markdown("<div style='text-align:left; margin-bottom:0.5rem; color:#222;'>Position your face in the center</div>", unsafe_allow_html=True)

        # Live camera input (uses browser camera)
        camera_file = st.camera_input('')

        if camera_file is not None:
            # Show the captured image inside the large card
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(camera_file, use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Save to session state for use elsewhere
            st.session_state['student_captured_photo'] = camera_file.getvalue()

            # Action buttons
            btn_col1, btn_col2 = st.columns([1,1])
            with btn_col1:
                if st.button('Use Photo', key='use_photo'):
                    st.success('Photo selected for attendance')
            with btn_col2:
                if st.button('Retake', key='retake_photo'):
                    # clear the stored photo and rerun
                    st.session_state.pop('student_captured_photo', None)
                    st.experimental_rerun()
                    
        else:
            # placeholder empty card when no camera yet
            st.markdown("<div class='card'><div style='height:360px;display:flex;align-items:center;justify-content:center;color:#777;'>Camera ready — click to take photo</div></div>", unsafe_allow_html=True)

    with right:
        # Small preview card
        preview = st.session_state.get('student_captured_photo', None)
        if preview:
            st.markdown("<div style='text-align:center; margin-top:40px;'><div class='card'>", unsafe_allow_html=True)
            st.image(preview, width=160)
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align:center; margin-top:40px;'><div class='card'><div style='width:160px;height:160px;display:flex;align-items:center;justify-content:center;color:#999;'>No preview</div></div></div>", unsafe_allow_html=True)

    footer_home()


if __name__ == '__main__':
    main()