import streamlit as st

# A dictionary to store user data (In a real app, this should be a database)
def initialize_users():
    if 'users' not in st.session_state:
        st.session_state.users = {}

# Registration component
import streamlit as st

def register_component():
    st.title("Register")

    # Add a unique key argument to each widget
    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")
    
    # Register button
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif username and email and password:
            # Here you would save the user's registration data to your database
            st.success(f"Account created successfully for {username}!")
        else:
            st.error("Please fill in all fields.")


# Login component
def login_component():
    st.subheader("Login")

    # Login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if user exists and the password matches
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Logged in successfully!")
        else:
            st.session_state.logged_in = False
            st.error("Invalid username or password.")
