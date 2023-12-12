import streamlit as st
import pyrebase
from app import lu

# Firebase initialization
firebaseConfig = {
    "apiKey": "AIzaSyCM-2QTRJPaDaPZnXRR5aSqkZRAIPFLaQg",
    "authDomain": "streamlit-cde99.firebaseapp.com",
    "databaseURL": "https://streamlit-cde99.firebaseio.com",
    "projectId": "streamlit-cde99",
    "storageBucket": "streamlit-cde99.appspot.com",
    "messagingSenderId": "651067602910",
    "appId": "1:651067602910:web:b98e16ab9aa07fd4000f4f",
    "measurementId": "G-XEQM0PYDYZ",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Function to authenticate user
def authenticate(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        return login
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to logout user
def logout():
    # Clear user info from session state
    st.session_state.user = None
    st.success("You have been logged out.")

def login():
    st.session_state.user = None
    st.success("Login successful.")

# Streamlit app content
def main():

    # Create a session state object
     if 'user' not in st.session_state:
        st.session_state.user = None

     if st.session_state.user is None:
        st.sidebar.markdown("<h1 style='text-align: center; color: black;'>LOGIN</h1>", unsafe_allow_html=True)

        email = st.sidebar.text_input("📧 Enter Your Email Address")
        password = st.sidebar.text_input("🔒 Enter Your Password", type="password")

        if st.sidebar.button("LOGIN"):
            if email and password:
                user = authenticate(email, password)
                if user:
                    st.sidebar.success("Login successful.")
                    st.session_state.user = user  # Store user info in session state
                else:
                    st.sidebar.error("Incorrect Email/Password")
            else:
                st.sidebar.warning("Please enter both email and password.")

        if st.sidebar.button("Forgot Password"):
            try:
                auth.send_password_reset_email(email)
                st.sidebar.success("Password reset email sent.")
            except Exception as e:
                st.sidebar.error(f"Error sending password reset email: {e}")

     else:
        pred.show_app()  # Show app content if the user is logged in

        if st.sidebar.button("Logout", on_click=logout):
            logout()  # Call the logout function to clear session state

if __name__ == "__main__":
    main()
