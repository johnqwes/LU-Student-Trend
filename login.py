import streamlit as st

def main():
    st.markdown("<h1 style='text-align: center;'>Welcome to LU Student Trend</h1>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://lu.edu.ph/wp-content/uploads/2016/11/cropped-lulogo.png",  use_column_width=True)

    with col2:
        st.markdown("<h1 style='text-align: center;'>🔐 LOGIN</h1>", unsafe_allow_html=True)
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email and password:
                # Your authentication logic here
                st.success("Login successful.")
            else:
                st.warning("Please enter both email and password.")

        if st.button("Forgot Password?"):
            # Logic for password reset
            st.success("Password reset email sent.")

if __name__ == "__main__":
    main()
