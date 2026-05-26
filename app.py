import streamlit as st

def main():
    st.header("hello this is title")
    name= st.text_input("Enter your name", key="name")
    col1,col2=st.columns(2)
    
    with col1:
    

        if st.button("display my name",type="primary",key="display",width="stretch"):
            st.write(f"Hello, {name}!")
    with col2:
        if st.button("byee",type="secondary",key="bye",width="stretch"):
            st.write(f"Goodbye, {name}!")
    
    st.markdown(
    """
    <div style="text-align:center;">
        <h1>Snap Class</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
    st.image("1.png", use_container_width=True)

main()