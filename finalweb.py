from pathlib import Path
import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import easyocr as ocr
import pandas as pd
import mysql.connector

# Function to create a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="2442003",
       # database="car_plates"
       database="car_plates_car_data.sql"
    )
# Function to search for data in the database
def search_data(conn, search_query):
    with conn.cursor() as cursor:
        query = "SELECT * FROM car_data WHERE plate_number LIKE %s OR plate_letters LIKE %s"
        values = ('%' + search_query + '%', '%' + search_query + '%')
        cursor.execute(query, values)
        result = cursor.fetchall()
    return result

# Function to add data to the database
def add_data(conn, plate_number, plate_letters, car_type, car_owner, governorate, chasset_number):
    try:
        query = "INSERT INTO car_data (plate_number, plate_letters, car_type, car_owner, governorate, chasset_number) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (plate_number, plate_letters, car_type, car_owner, governorate, chasset_number)
        with conn.cursor() as cursor:
            cursor.execute(query, values)
        conn.commit()
        st.success("Data added successfully!")
    except Exception as e:
        st.error(f"Error: {e}")
        conn.rollback()

# YOLOv3 object detection
model_yolo = None
confidence_yolo = 0.4

def load_model_yolo(model_path):
    return YOLO(model_path)

def detect_objects(image):
    if model_yolo is None:
        return None

    pil_image = Image.open(image)
    np_image = np.array(pil_image)
    results = model_yolo(np_image, conf=confidence_yolo, hide_conf=True)
    annotated_image = results[0].plot()
    return annotated_image

# EasyOCR text extraction
@st.cache
def load_model_ocr():
    return ocr.Reader(['ar','en'], model_storage_directory=r"D:\car_plate_detection\car plates-\Automatic-number-plate-recognition-in-real-time-")

model_ocr = load_model_ocr()

# Streamlit App
st.title("Car Plates Database Management with Object Detection")

# Connect to the database
conn = connect_to_database()

# Initialize YOLOv3 model
model_path_yolo = Path(r"D:\car_plate_detection\car plates-\Automatic-number-plate-recognition-in-real-time-\best.pt")
model_yolo = load_model_yolo(model_path_yolo)

# Streamlit app
st.header("Upload an Image for Object Detection and Database Search")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "webp"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Detect objects in the image using YOLOv3
    detected_image_yolo = detect_objects(uploaded_file)
    if detected_image_yolo is not None:
        st.image(detected_image_yolo, caption="Detected Objects (YOLO).", use_column_width=True)

    # Extract text from the image using EasyOCR
    input_image_ocr = Image.open(uploaded_file)
    result_ocr = model_ocr.readtext(np.array(input_image_ocr))

    result_text_ocr = []
    for text in result_ocr:
        result_text_ocr.append(text[1])

    st.write("OCR Results:", result_text_ocr)

   

# Search the database for matching records
if st.button("Search Database"):
    for search_query in result_text_ocr:
        search_result = search_data(conn, search_query)
        if search_result:
            st.success(f"Search Results for: {search_query}")
            for record in search_result:
                st.info(
                    f"ID: {record[0]},\nPlate Number: {record[1]},\nPlate Letters: {record[2]},\nCar Type: {record[3]},\nCar Owner: {record[4]},\nGovernorate: {record[5]},\nChassis Number: {record[6]}"
                )
        else:
            st.warning(f"No matching records found for: {search_query}")

    # Streamlit form to add data
    st.header("Add Data to the Database")

    plate_number = st.text_input("Plate Number:")
    plate_letters = st.text_input("Plate Letters:")
    car_type = st.text_input("Car Type:")
    car_owner = st.text_input("Car Owner:")
    governorate = st.text_input("Governorate:")
    chasset_number = st.text_input("Chassis Number:")

    if st.button("Add Data"):
        add_data(conn, plate_number, plate_letters, car_type, car_owner, governorate, chasset_number)
    
    st.balloons()

# Close the database connection
conn.close()