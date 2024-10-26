import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import datetime

# Load existing announcements or create a new one
def load_announcements():
    try:
        announcements = pd.read_csv("announcements.csv")
    except FileNotFoundError:
        announcements = pd.DataFrame(columns=["Date", "Title", "Content"])
    return announcements

# Display the main announcement board
def display_main_announcement_board(announcements):
    st.title("Event and Announcement Board")
    st.subheader("All Announcements:")
    st.table(announcements)

# Add a new announcement
def add_announcement():
    st.subheader("Add Announcement:")
    date = st.date_input("Date:", datetime.date.today())
    title = st.text_input("Title:")
    content = st.text_area("Content:")

    add_button_key = "add_announcement_button"

    if st.button("Post Announcement", key=add_button_key, help="Click to post the announcement"):
        new_announcement = pd.DataFrame({
            "Date": [date],
            "Title": [title],
            "Content": [content]
        })

        announcements = load_announcements()
        announcements = pd.concat([announcements, new_announcement], ignore_index=True)
        announcements.to_csv("announcements.csv", index=False)
        st.success("Announcement posted successfully!")

# Update an existing announcement
def update_announcement(announcements):
    st.subheader("Update Announcement:")
    st.table(announcements)

    index_to_update = st.number_input("Enter the index to update:", min_value=0, max_value=len(announcements) - 1,
                                      step=1)
    updated_title = st.text_input("Updated Title:", announcements.at[index_to_update, "Title"])
    updated_content = st.text_area("Updated Content:", announcements.at[index_to_update, "Content"])

    # Separate button for update
    update_button_key = "update_announcement_button"
    if st.button("Update Announcement", key=update_button_key, help="Click to update the announcement"):
        announcements.at[index_to_update, "Title"] = updated_title
        announcements.at[index_to_update, "Content"] = updated_content

        announcements.to_csv("announcements.csv", index=False)
        st.success("Announcement updated successfully!")

# Function to read user data from CSV file
def read_user_data(file_path="user_data.csv"):
    try:
        user_data = pd.read_csv(file_path)
        return user_data
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Password"])

# Function to save user data to CSV file
def save_user_data(user_data, file_path="user_data.csv"):
    user_data.to_csv(file_path, index=False)

# Function to show the main content after logging in
def show_main_content():
    st.header('Event and Announcement Board ', divider='green')
    announcements = load_announcements()

    selected_option = st.sidebar.radio("Select Option:",
                                       ["Post Announcement", "View All Announcements", "Update Announcement"])

    if selected_option == "Post Announcement":
        add_announcement()
    elif selected_option == "View All Announcements":
        display_main_announcement_board(announcements)
    elif selected_option == "Update Announcement":
        update_announcement(announcements)

    st.divider()

# Function to handle login
def login_page(user_data, session_state):
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if not username or not password:
        st.error("Please enter both username and password.")
        return

    if st.button("Login"):
        user_row = user_data[user_data["Username"] == username.strip()]
        if not user_row.empty and str(user_row["Password"].iloc[0]).strip() == password:
            session_state.login_status = "success"
            st.success(f"Welcome back, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password. Please try again.")

# Function to handle registration
def register_page(user_data, session_state):
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username in user_data["Username"].values:
            st.error("Username already exists. Please choose a different username.")
        else:
            new_user = pd.DataFrame({"Username": [username], "Password": [password]})
            user_data = pd.concat([user_data, new_user], ignore_index=True)
            save_user_data(user_data)
            session_state.login_status = "success"
            st.success(f"Registration successful! Welcome, {username}!")

# Main function
def main():
    user_data = read_user_data()

    session_state = st.session_state
    if not hasattr(session_state, 'login_status'):
        session_state.login_status = None

    if session_state.login_status != "success":
        selected = option_menu(
            menu_title=None,
            options=["Login", "Register"],
            default_index=0,
            orientation="horizontal",
        )

        if selected == "Login":
            login_page(user_data, session_state)
        elif selected == "Register":
            register_page(user_data, session_state)
    else:
        st.markdown("")  # Empty Markdown element to clear previous content
        main_content_placeholder = st.empty()
        show_main_content()
        main_content_placeholder.markdown("")

if __name__ == "__main__":
    main()
