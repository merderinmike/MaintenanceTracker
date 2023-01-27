import pandas
import streamlit as st
from db_create import *
from bson.objectid import ObjectId
#---Page setup---
title = st.title('Vehicle Maintenance Tracker')
header = st.subheader('Here you can view, edit, and create Maintenance information related to your specific vehicle')
tab1, tab2, tab3 = st.tabs(["Add record", "View record", "Add Vehicle"])

#---Add Record---
with tab1:
    with st.form('addrecord', clear_on_submit=True):
        vehicle = st.selectbox(
            "Select a vehicle to add a record: ", (selection)
        )
        miles = st.number_input("Enter miles of vehicle", key="miles", value=0, )
        date = str(st.date_input("What was the date of Maintenance? "))
        tasks = st.text_area("Tasks", placeholder="What tasks were performed? ")
        if st.form_submit_button("submit"):
            records.insert_one({"model": vehicle, "miles":miles, "date": date , "tasks":tasks})
            st.success("Record created")
#---View Record---
with tab2:
    with st.form("viewRecord"):
        records = st.selectbox(
            '',
            (recordModel)
        )
        "---"
        if st.form_submit_button("submit"):
            st.table(data=df)
#---Add Vehicle---
with tab3:
    with st.form("addVehicle", clear_on_submit=True):
        make = st.text_input("Please enter the vehicle make: ", key="make")
        model = st.text_input("Please enter the vehicle model: ", key="model")
        year = st.number_input("Please enter the vehicle year: ",key="year" ,value=0)
        submit = st.form_submit_button("submit")
        if submit:
            if vehicles.count_documents({ 'model': model }) != 0:
                st.exception("Vehicle already exists!")
            else:
                vehicles.insert_one({"make": make, "model": model, "year": year})
                st.success("Vehicle submitted")


#if db.collection.count_documents({ 'UserIDS': newID }, limit = 1):