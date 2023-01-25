import streamlit as st
from db_create import *

#---Page setup---
title = st.title('Vehicle Maintenance Tracker')
header = st.subheader('Here you can view, edit, and create Maintenance information related to your specific vehicle')
tab1, tab2, tab3 = st.tabs(["Add record", "View record", "Add Vehicle"])
#---Add Record---
with tab1:
    vehicle = st.selectbox(
        "Select a vehicle to add a record: ",
        ()
    )
    date = st.date_input("What was the date of Maintenance? ")
    comment = st.text_area("Comments", placeholder="Please enter a comment")
#---View Record---
with tab2:
    record = st.selectbox(
        '',
        ('Select','option1', 'option2', 'option3')
    )
    "---"
    if 'option1' in record:
        st.write("You chose option 1!")
#---Add Vehicle---
with tab3:
    with st.form("addVehicle", clear_on_submit=True):
        make = st.text_input("Please enter the vehicle make: ", key="make")
        model = st.text_input("Please enter the vehicle model: ", key="model")
        year = st.number_input("Please enter the vehicle year: ",key="year" ,value=0)
        submit = st.form_submit_button("submit")
        if submit:
            if model not in collection:
                if year not in collection:
                    collection = db[model]
                    collection.insert_one({""})
            st.success("Vehicle submitted")
        st.write(make, model, year)
