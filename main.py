import sqlite3
import streamlit as st

def init_db():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT)''')
    conn.commit()
    conn.close()

def add_contact(name, phone, email):
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()

def view_contacts():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return contacts

def search_contact(name):
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + name + '%',))
    contacts = c.fetchall()
    conn.close()
    return contacts

def update_contact(contact_id, name, phone, email):
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?", (name, phone, email, contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()

# Initialize the database
init_db()

st.title("📇 Contact Management System")

menu = ["Add Contact", "View Contacts", "Search Contact", "Update Contact", "Delete Contact"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Contact":
    st.subheader("Add a New Contact")
    with st.form("add_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Contact")
        if submitted:
            add_contact(name, phone, email)
            st.success(f"Contact {name} added successfully!")

elif choice == "View Contacts":
    st.subheader("All Contacts")
    contacts = view_contacts()
    for contact in contacts:
        st.write(f"ID: {contact[0]} | Name: {contact[1]} | Phone: {contact[2]} | Email: {contact[3]}")

elif choice == "Search Contact":
    st.subheader("Search for a Contact")
    search_term = st.text_input("Enter name to search")
    if st.button("Search"):
        results = search_contact(search_term)
        if results:
            for contact in results:
                st.write(f"ID: {contact[0]} | Name: {contact[1]} | Phone: {contact[2]} | Email: {contact[3]}")
        else:
            st.warning("No contacts found!")

elif choice == "Update Contact":
    st.subheader("Update Contact Details")
    contact_id = st.number_input("Enter Contact ID", min_value=1, step=1)
    new_name = st.text_input("New Name")
    new_phone = st.text_input("New Phone")
    new_email = st.text_input("New Email")
    if st.button("Update Contact"):
        update_contact(contact_id, new_name, new_phone, new_email)
        st.success(f"Contact ID {contact_id} updated successfully!")

elif choice == "Delete Contact":
    st.subheader("Delete a Contact")
    contact_id = st.number_input("Enter Contact ID", min_value=1, step=1)
    if st.button("Delete Contact"):
        delete_contact(contact_id)
        st.error(f"Contact ID {contact_id} deleted successfully!")
