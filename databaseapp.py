import streamlit as st
import pandas as pd
import mysql.connector
import re

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

# Function to determine governorate based on plate number and letters
def determine_governorate(plate_number, plate_letters):
    if len(re.findall(r'\d', plate_number)) == 3 and len(plate_letters) == 3:
        return "Cairo"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 2:
        return "Giza"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'س':
        return "Alex"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ب':
        return "Beheira"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ف':
        return "Fayoum"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ر':
        return "Sharqia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ل':
        return "Kafr El Sheikh"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'و':
        return "Beni Suef"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'د':
        return "Dakahlia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ع':
        return "Gharbia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ن':
        return "Minya"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'م':
        return "Monufia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ق':
        return "Qalyubia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ي':
        return "Asyut"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ه':
        return "Sohag"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ج' and plate_letters[1] == 'ه':
        return "Matrouh"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ج' and plate_letters[1] == 'ب':
        return "El Wadi El Gedid"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ص' and plate_letters[1] == 'أ':
        return "Qena"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ص' and plate_letters[1] == 'ق':
        return "Luxor"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ص' and plate_letters[1] == 'و':
        return "Aswan"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'س':
        return "Suez"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ص':
        return "Ismailia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ع':
        return "Port Said"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'د':
        return "Dameitta"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'أ':
        return "North Sinai"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ج':
        return "South Sinai"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ر':
        return "Red Sea"
    else:
        return "Unknown"

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
governorate = determine_governorate(plate_number, plate_letters) if plate_number and plate_letters else ""
# Disable the governorate field
st.text_input("Governorate:", value=governorate, disabled=True)
chassis_number = st.text_input("Chassis Number:")
email = st.text_input("Email:")
irregularities = st.checkbox("Irregularities")
irregularities_reason = st.text_area("Irregularities Reason") if irregularities else ""

if st.button("Add Data"):
    add_data(conn, plate_number, plate_letters, car_type, car_owner, governorate, chassis_number, email, irregularities, irregularities_reason)

# Search functionality
st.header("Search Data")
search_query = st.text_input("Enter Plate Number or Letters:")
if st.button("Search"):
    search_results = search_data(conn, search_query)
    st.write(pd.DataFrame(search_results, columns=["ID", "Plate Number", "Plate Letters", "Car Type", "Car Owner", "Governorate", "Chassis Number", "Email", "Irregularities", "Irregularities Reason", "Paid Status", "Cost"]))

# Display all data
st.header("All Data in the Database")
data = get_data(conn)
# Print out the data to understand its structure
st.write(data)
# Create DataFrame only if data is present
if data:
    st.write(pd.DataFrame(data, columns=["ID", "Plate Number", "Plate Letters", "Car Type", "Car Owner", "Governorate", "Chassis Number", "Email", "Irregularities", "Irregularities Reason", "Paid Status", "Cost"]))

# Streamlit form to update data
st.header("Update Data in the Database")
record_id = st.number_input("Record ID:", min_value=1, step=1)
irregularities = st.checkbox("Irregularities", key="update_irregularities")
irregularities_reason = st.text_area("Irregularities Reason", key="update_irregularities_reason") if irregularities else ""
paid_status = st.checkbox("Paid Status")
cost = st.number_input("Cost:", min_value=0, step=1)

if st.button("Update Data"):
    update_data(conn, record_id, irregularities, irregularities_reason, paid_status, cost)

# Close the database connection
conn.close()
