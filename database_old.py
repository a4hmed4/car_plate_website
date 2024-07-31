import streamlit as st
import pandas as pd
import mysql.connector

# Function to create a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="2442003",
        database="car_plates"
    )

# Function to add data to the database
def add_data(conn, plate_number, plate_letters, car_type, car_owner, governorate, chassis_number, email, irregularities, irregularities_reason):
    try:
        query = "INSERT INTO car_data (plate_number, plate_letters, car_type, car_owner, governorate, chassis_number, email, irregularities, irregularities_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (plate_number, plate_letters, car_type, car_owner, governorate, chassis_number, email, irregularities, irregularities_reason)
        with conn.cursor() as cursor:
            cursor.execute(query, values)
        conn.commit()
        st.success("Data added successfully!")
    except Exception as e:
        st.error(f"Error: {e}")
        conn.rollback()

# Function to search for data in the database
def search_data(conn, search_query):
    with conn.cursor() as cursor:
        query = "SELECT * FROM car_data WHERE plate_number LIKE %s OR plate_letters LIKE %s"
        values = ('%' + search_query + '%', '%' + search_query + '%')
        cursor.execute(query, values)
        result = cursor.fetchall()
    return result

# Function to retrieve data from the database
def get_data(conn):
    with conn.cursor() as cursor:
        query = "SELECT * FROM car_data"
        cursor.execute(query)
        result = cursor.fetchall()
    return result

# Function to update irregularities and payment status
def update_data(conn, record_id, irregularities, irregularities_reason, paid_status, cost):
    try:
        query = """
        UPDATE car_data
        SET irregularities = %s, irregularities_reason = %s, paid_status = %s, cost = %s
        WHERE id = %s
        """
        values = (irregularities, irregularities_reason, paid_status, cost, record_id)
        with conn.cursor() as cursor:
            cursor.execute(query, values)
        conn.commit()
        st.success("Data updated successfully!")
    except Exception as e:
        st.error(f"Error: {e}")
        conn.rollback()

# Streamlit App
st.title("Car Plates Database Management")

# Connect to the database
conn = connect_to_database()

# Streamlit form to add data
st.header("Add Data to the Database")

plate_number = st.text_input("Plate Number:")
plate_letters = st.text_input("Plate Letters:")
car_type = st.text_input("Car Type:")
car_owner = st.text_input("Car Owner:")
governorate = st.text_input("Governorate:")
chassis_number = st.text_input("Chassis Number:")
email = st.text_input("Email:")
irregularities = st.checkbox("Irregularities")
irregularities_reason = st.text_area("Irregularities Reason") if irregularities else ""

if st.button("Add Data"):
    add_data(conn, plate_number, plate_letters, car_type, car_owner, governorate, chassis_number, email, irregularities, irregularities_reason)

# Streamlit search form
st.header("Search Data in the Database")
search_query = st.text_input("Search by Plate Number or Letters:")
if st.button("Search"):
    search_result = search_data(conn, search_query)
    st.header("Search Results:")
    if not search_result:
        st.info("No matching records found.")
    else:
        for record in search_result:
            st.text(f"ID: {record[0]}, Plate Number: {record[1]}, Plate Letters: {record[2]}, Car Type: {record[3]}, Car Owner: {record[4]}, Governorate: {record[5]}, Chassis Number: {record[6]}, Email: {record[7]}, Irregularities: {record[8]}, Irregularities Reason: {record[9]}")
            if st.button(f"Edit Record ID {record[0]}", key=f"edit_{record[0]}"):
                st.session_state["edit_record_id"] = record[0]
                st.session_state["edit_irregularities"] = record[8]
                st.session_state["edit_irregularities_reason"] = record[9]
                st.session_state["edit_paid_status"] = record[10] if len(record) > 10 else False
                st.session_state["edit_cost"] = record[11] if len(record) > 11 else 0

# Streamlit form to edit data
if "edit_record_id" in st.session_state:
    st.header("Edit Data in the Database")
    
    irregularities = st.checkbox("Irregularities", value=st.session_state["edit_irregularities"])
    irregularities_reason = st.text_area("Irregularities Reason", value=st.session_state["edit_irregularities_reason"]) if irregularities else ""
    paid_status = st.checkbox("Paid Status", value=st.session_state["edit_paid_status"])
    cost = st.number_input("Cost", value=st.session_state["edit_cost"])

    if st.button("Update Data"):
        update_data(conn, st.session_state["edit_record_id"], irregularities, irregularities_reason, paid_status, cost)
        del st.session_state["edit_record_id"]
        del st.session_state["edit_irregularities"]
        del st.session_state["edit_irregularities_reason"]
        del st.session_state["edit_paid_status"]
        del st.session_state["edit_cost"]

# Display current data in the database
st.header("Current Data in the Database")
result = get_data(conn)

# Determine if the extra columns exist
columns = ["ID", "Plate Number", "Plate Letters", "Car Type", "Car Owner", "Governorate", "Chassis Number", "Email", "Irregularities", "Irregularities Reason"]
if result and len(result[0]) > 10:
    columns += ["Paid Status", "Cost"]

df = pd.DataFrame(result, columns=columns)

st.dataframe(df)

# Close the database connection
conn.close()


