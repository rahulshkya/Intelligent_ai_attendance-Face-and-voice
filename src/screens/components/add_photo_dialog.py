import streamlit as st
from database.db import create_subject
from PIL import Image

@st.dialog('Capture or upload photos')
def add_photo_dialog():
    st.write('Add classroom photos to scan for attendance')
    

    if 'photo_tab' not in st.session_state:
        st.session_state['photo_tab'] = 'camera'

    t1,t2=st.columns(2)

    with t1:
        type_camera='primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('camera' , type= type_camera,width='stretch'):
            st.session_state.photo_tab ='camera'

    with t2:
        type_upload='primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('upload',type= type_upload,width='stretch'):
            st.session_state.photo_tab ='upload'
        
    if 'last_camera_photo' not in st.session_state:
        st.session_state.last_camera_photo = None

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input(
            "Take a photo",
            key='camera_input'
        )

        if cam_photo:
            photo_id = cam_photo.file_id

            if photo_id != st.session_state.last_camera_photo:
                st.session_state.attendence_image.append(
                    Image.open(cam_photo).convert('RGB')
                )

                st.session_state.last_camera_photo = photo_id
                st.toast("Photo added successfully!")
    
    if st.session_state.photo_tab == 'upload':
        upload_photo=st.file_uploader("Upload a photo",type=['jpg','jpeg','png'],key='upload_input',accept_multiple_files=True)
        if upload_photo:
            for photo in upload_photo:
                st.session_state.attendence_image.append(Image.open(photo).convert('RGB'))
            st.toast("Photos added successfully!")
            st.rerun()

    st.divider()
    if st.button("Done",type='primary',width='stretch'):
    
        st.rerun()