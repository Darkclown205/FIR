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
    user = next((user for user in users if user['username']
                == username and user['password'] == password), None)
    return user

# User registration


def register(username, password, role):
    users = load_users()
    if any(user['username'] == username for user in users):
        return False
    users.append({"username": username, "password": password, "role": role})
    save_users(users)
    return True


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['role'] = None

    st.title('Online FIR System')

    menu = ["Login", "Register", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            user = authenticate(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['role'] = user['role']
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        role = st.selectbox("Role", options=["user", "cops"])  # Role selection

        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords do not match")
            elif register(username, password, role):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists")

    elif choice == "Dashboard":
        if not st.session_state['logged_in']:
            st.warning("Please login to access the dashboard")
            return

        st.subheader("FIR Dashboard")

        firs = load_data()

        if st.session_state['role'] == 'user':
            with st.form(key='fir_form'):
                complainer_name = st.text_input("Your Name")
                complainer_email = st.text_input("Your Email")
                title = st.text_input("Title")
                description = st.text_area("Description")
                location = st.text_input("Location")
                action_requested = st.text_input("Action Requested")
                evidence = st.file_uploader("Upload Evidence", type=['jpg', 'png', 'pdf'])
                declaration = st.checkbox(
                    "I declare that the information provided is true and accurate.")
                submit_button = st.form_submit_button(label='Add FIR')

                if submit_button:
                    if not declaration:
                        st.error("You must declare that the information is true and accurate.")
                    elif title and description and location and action_requested and complainer_name and complainer_email:
                        fir_id = len(firs) + 1
                        fir_data = {
                            "id": fir_id,
                            "complainer_name": complainer_name,
                            "complainer_email": complainer_email,
                            "title": title,
                            "description": description,
                            "location": location,
                            "action_requested": action_requested,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "Open"
                        }
                        if evidence:
                            evidence_path = os.path.join(
                                'data', f'evidence_{fir_id}_{evidence.name}')
                            with open(evidence_path, 'wb') as file:
                                file.write(evidence.read())
                            fir_data["evidence"] = evidence_path
                        firs.append(fir_data)
                        save_data(firs)
                        st.success("FIR added successfully!")
                    else:
                        st.error("Please fill all required fields.")

        elif st.session_state['role'] == 'cops':
            search = st.text_input("Search FIRs by title, location, or status")
            filtered_firs = [fir for fir in firs if search.lower() in fir['title'].lower(
            ) or search.lower() in fir['location'].lower() or search.lower() in fir['status'].lower()]

            st.write("### All FIRs")
            for fir in filtered_firs:
                st.write(
                    f"**{fir['title']}**: {fir['description']} (Location: {fir['location']}, Action Requested: {fir['action_requested']}, Status: {fir['status']}, Time: {fir['timestamp']})")
                st.write(f"Complainer: {fir['complainer_name']}")

                if "evidence" in fir:
                    with open(fir['evidence'], 'rb') as file:
                        st.download_button(
                            label="Download Evidence",
                            data=file,
                            file_name=os.path.basename(fir['evidence']),
                            mime="application/octet-stream"
                        )

                if fir['status'] == 'Open':
                    close_button = st.button(f"Close FIR {fir['id']}", key=f"close_{fir['id']}")
                    if close_button:
                        fir['status'] = 'Closed'
                        fir['closed_by'] = st.session_state['username']
                        fir['closed_on'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # Notify complainer (you might want to send an email in a real app)
                        st.success(
                            f"Case {fir['id']} closed by {fir['closed_by']} on {fir['closed_on']}")
                        st.info(
                            f"Notification sent to complainer: {fir['complainer_name']} at {fir['complainer_email']}")
                        save_data(firs)


if __name__ == "__main__":
    main()


# Save users data
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# User authentication
def authenticate(username, password):
    users = load_users()
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    return user

# User registration
def register(username, password, role):
    users = load_users()
    if any(user['username'] == username for user in users):
        return False
    users.append({"username": username, "password": password, "role": role})
    save_users(users)
    return True

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['role'] = None

    st.title('Online FIR System')

    menu = ["Login", "Register", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            user = authenticate(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['role'] = user['role']
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        role = st.selectbox("Role", options=["user", "cops"])  # Role selection

        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords do not match")
            elif register(username, password, role):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists")

    elif choice == "Dashboard":
        if not st.session_state['logged_in']:
            st.warning("Please login to access the dashboard")
            return

        st.subheader("FIR Dashboard")

        firs = load_data()

        if st.session_state['role'] == 'user':
            with st.form(key='fir_form'):
                complainer_name = st.text_input("Your Name")
                complainer_email = st.text_input("Your Email")
                title = st.text_input("Title")
                description = st.text_area("Description")
                location = st.text_input("Location")
                action_requested = st.text_input("Action Requested")
                evidence = st.file_uploader("Upload Evidence", type=['jpg', 'png', 'pdf'])
                declaration = st.checkbox("I declare that the information provided is true and accurate.")
                submit_button = st.form_submit_button(label='Add FIR')

                if submit_button:
                    if not declaration:
                        st.error("You must declare that the information is true and accurate.")
                    elif title and description and location and action_requested and complainer_name and complainer_email:
                        fir_id = len(firs) + 1
                        fir_data = {
                            "id": fir_id,
                            "complainer_name": complainer_name,
                            "complainer_email": complainer_email,
                            "title": title,
                            "description": description,
                            "location": location,
                            "action_requested": action_requested,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "Open"
                        }
                        if evidence:
                            evidence_path = os.path.join('data', f'evidence_{fir_id}_{evidence.name}')
                            with open(evidence_path, 'wb') as file:
                                file.write(evidence.read())
                            fir_data["evidence"] = evidence_path
                        firs.append(fir_data)
                        save_data(firs)
                        st.success("FIR added successfully!")
                    else:
                        st.error("Please fill all required fields.")

        elif st.session_state['role'] == 'cops':
            search = st.text_input("Search FIRs by title, location, or status")
            filtered_firs = [fir for fir in firs if search.lower() in fir['title'].lower() or search.lower() in fir['location'].lower() or search.lower() in fir['status'].lower()]

            st.write("### All FIRs")
            for fir in filtered_firs:
                st.write(f"**{fir['title']}**: {fir['description']} (Location: {fir['location']}, Action Requested: {fir['action_requested']}, Status: {fir['status']}, Time: {fir['timestamp']})")
                st.write(f"Complainer: {fir['complainer_name']}")

                if "evidence" in fir:
                    with open(fir['evidence'], 'rb') as file:
                        st.download_button(
                            label="Download Evidence",
                            data=file,
                            file_name=os.path.basename(fir['evidence']),
                            mime="application/octet-stream"
                        )

                if fir['status'] == 'Open':
                    close_button = st.button(f"Close FIR {fir['id']}", key=f"close_{fir['id']}")
                    if close_button:
                        fir['status'] = 'Closed'
                        fir['closed_by'] = st.session_state['username']
                        fir['closed_on'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # Notify complainer (you might want to send an email in a real app)
                        st.success(f"Case {fir['id']} closed by {fir['closed_by']} on {fir['closed_on']}")
                        st.info(f"Notification sent to complainer: {fir['complainer_name']} at {fir['complainer_email']}")
                        save_data(firs)

if __name__ == "__main__":
    main()
