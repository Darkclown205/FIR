import streamlit as st
import json
import os
from datetime import datetime

# Define file paths
DATA_FILE = 'data/firs.json'
USERS_FILE = 'data/users.json'

# Load FIRs data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Save FIRs data
def save_data(firs):
    with open(DATA_FILE, 'w') as file:
        json.dump(firs, file, indent=4)

# Load users data
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save users data
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# User authentication
def authenticate(username, password):
    users = load_users()
    return any(user['username'] == username and user['password'] == password for user in users)

# User registration
def register(username, password):
    users = load_users()
    if any(user['username'] == username for user in users):
        return False
    users.append({"username": username, "password": password})
    save_users(users)
    return True

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None

    st.title('Online FIR System')

    menu = ["Login", "Register", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        
        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords do not match")
            elif register(username, password):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists")
    
    elif choice == "Dashboard":
        if not st.session_state['logged_in']:
            st.warning("Please login to access the dashboard")
            return
        
        st.subheader("FIR Dashboard")

        firs = load_data()

        with st.form(key='fir_form'):
            title = st.text_input("Title")
            description = st.text_area("Description")
            location = st.text_input("Location")
            submit_button = st.form_submit_button(label='Add FIR')

            if submit_button and title and description and location:
                firs.append({
                    "id": len(firs) + 1,
                    "title": title,
                    "description": description,
                    "location": location,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "Open"
                })
                save_data(firs)
                st.success("FIR added successfully!")

        st.write("### All FIRs")
        for fir in firs:
            st.write(f"**{fir['title']}**: {fir['description']} (Location: {fir['location']}, Status: {fir['status']}, Time: {fir['timestamp']})")
            if st.button(f"Delete FIR {fir['id']}", key=f"delete_{fir['id']}"):
                firs = [f for f in firs if f['id'] != fir['id']]
                save_data(firs)
                st.success(f"FIR {fir['id']} deleted successfully!")

if __name__ == "__main__":
    main()
