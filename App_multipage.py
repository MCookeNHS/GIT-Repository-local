import streamlit as st
#from 2_app_page_1 import page1
#from 2_app_page_2 import page2

# Create a sidebar for page navigation
# page = st.sidebar.selectbox("Select a page", ("Page 1", "Page 2"))
#
# # Display the selected page
# if page == "Page 1":
#     page1()
# elif page == "Page 2":
#     page2()
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
st.sidebar.header("Welcome")
st.title("simulation tester")
st.write("here is text about the site")
st.sidebar.success("Select a demo above.")
# tab1, tab2 = st.tabs(["Page 1", "Page 2"])
# with tab1:
#     page1()
# with tab2:
#     page2()