import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time
import db

page_title = "Stock/ETF portfolio analytics"
layout = "centered"
st.set_page_config(page_title=page_title, layout=layout, initial_sidebar_state="collapsed")
st.title(f"{page_title}")

# generic streamlit configuration to hide brandings
hide_st_style = """<style>
                #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                header {visibility : hidden;}
                </style>
                """
hide_sidebar_hamburger =  """
                        <style>
                            [data-testid="collapsedControl"] {
                                display: none
                            }
                        </style>
                        """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(hide_sidebar_hamburger,unsafe_allow_html=True,)

with st.form("login_form", clear_on_submit=True):
        st.text_input("**Username:** `required`", key="username")
        st.text_input("**Password:** `required`", key="password", type="password")
       
        login_button = st.form_submit_button("Login", type = "primary")
        
if login_button:
    if st.session_state["username"] != "":
        if db.authenticate_user(st.session_state["username"], st.session_state["password"]):
            st.info("Login successful")
            time.sleep(0.5)
            st.session_state['uuid'] = st.session_state["username"]
            switch_page("app")
        else:
            st.error("Incorrect username or password")
    else:
        st.error("Please input username and password")

with st.expander("New user? Register here"):
    with st.form("entry_form", clear_on_submit=True):
        st.text_input("**Username:** `required`", key="register.username")
        st.text_input("**Email:**", key="register.email")
        st.text_input("**Password:** `required`", key="register.password1", type="password")
        st.text_input("**Verify Password:** `required`", key="register.password2", type="password")
       
        register_button = st.form_submit_button("Register", type = "primary")
        
    if register_button:
        if 'register.username' in st.session_state and "register.password1" in st.session_state:
            if db.check_if_username_available(st.session_state["register.username"]):
                if st.session_state["register.password1"] == st.session_state["register.password2"]:
                    db.register_user(st.session_state["register.username"], st.session_state["register.email"], st.session_state["register.password1"])
                    st.info("Registration Successful")
                    st.session_state['uuid'] = st.session_state["register.username"]
                    switch_page("app")
                else:
                    st.error("Passwords donot match. Try again")
            else:
                st.error("Username already registered, try another username") 
        else:
            st.error("Please specify a username")
