import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client using Streamlit secrets
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

st.title("WINTER ARC TRACKER")

# Check if user is already logged in
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.subheader("Sign In or Create Account")
    
    auth_mode = st.radio("Choose action", ["Log In", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Submit"):
        try:
            if auth_mode == "Sign Up":
                response = supabase.auth.sign_up({"email": email, "password": password})
                st.success("Account created successfully! You can now log in.")
            else:
                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = response.user
                st.success("Logged in successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"Authentication failed: {e}")
else:
    st.write(f"Welcome back, {st.session_state.user.email}!")
    
    if st.button("Log Out"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
        
    # --- PUT YOUR WINTER ARC TRACKER APP CODE HERE ---
    st.info("You are logged in and ready to track your progress!")
