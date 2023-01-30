import pandas as pd
import time
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

# ----DB setup---
load_dotenv(find_dotenv())
password = st.secrets["MONGOPW"]
cluster = MongoClient(
    f"""mongodb+srv://ashehorn:{password}@cluster0.4miwcyq.mongodb.net/?retryWrites=true&w=majority""")

db = cluster["Maintenance"]
vehicles = db["Vehicles"]
records = db['Records']
findVehicle = list(vehicles.find())
selection = []
recordModel = []
record = []
for item in findVehicle:
    selection.append(f"{item['model']}")
selection.insert(0, "Select a vehicle")
# ---Page setup---
st.set_page_config(
    page_title="Maintenance Tracker",
    page_icon="🔧"
)
title = st.title('Vehicle Maintenance Tracker')
header = st.subheader('Here you can view, edit, and create Maintenance information related to your specific vehicle')
tab1, tab2, tab3, tab4 = st.tabs(["Add record", "View record", "Add Vehicle", "Remove Vehicle"])
col1, col2 = st.columns(2)
# ---Add Record---
with tab1:
    with st.form('addrecord', clear_on_submit=True):
        vehicle = st.selectbox(
            "Select a vehicle to add a record: ", selection
        )
        miles = str(st.number_input("Enter miles of vehicle", key="miles", value=0, ))
        date = str(st.date_input("What was the date of Maintenance? "))
        tasks = st.text_area("Tasks", placeholder="What tasks were performed? ")
        parts = st.text_area("Enter what parts were used for this task (If none leave blank)")
        cost = st.number_input("Enter total cost of task (Include any tools needed to complete task)", value=0,
                               min_value=0)
        if st.form_submit_button("submit"):
            records.insert_one(
                {"model": vehicle, "miles": miles, "date": date, "tasks": tasks, "parts": parts, "cost": cost})
            st.success("Record created")
# ---view/edit/remove record---
with tab2:
    recordselect = st.selectbox(
        "Select a vehicle to view record", selection)
    "---"
    x = []
    findRecord = list(records.find({'model': recordselect}, {"_id": 0}))
    for entry in findRecord:
        x.append(entry)
    df = pd.DataFrame(x)
    st.table(df)

    action = st.selectbox("Edit or Remove a record?", ["Make Selection", "Edit", "Remove"])
    if action == "Edit":
        lst = []
        with st.form("Edit", clear_on_submit=True):
            findRecord = list(records.find({'model': recordselect}, {"_id": 0}))
            for x in findRecord:
                lst.append(x)
            recordEdit = st.selectbox("Select your record", [lst[0]['tasks']])
            tasks = st.text_area("Tasks", placeholder="What tasks were performed? ", key="tasks1")
            miles = str(st.number_input("Enter miles of vehicle", key="miles1", value=0, ))
            parts = st.text_area("Enter what parts were used for this task (If none leave blank)", key="parts1")
            cost = st.number_input("Enter total cost of task (Include any tools needed to complete task)", key="cost1",
                                   value=0,
                                   min_value=0)
            records.update_many({"$and": [{"model": recordselect}, {"date": recordEdit}]},
                                {"$set": {"miles": miles, "tasks": tasks, "parts": parts, "cost": cost}})
            if st.form_submit_button("Submit"):
                st.experimental_rerun()
    elif action == "Remove":
        with st.form("Remove", clear_on_submit=True):
            recordRemove = st.text_input("Enter the date of the record you wish to edit from the table above: ")
            records.delete_one({"date": recordRemove})
            if st.form_submit_button("Submit"):
                st.experimental_rerun()
# ---Add Vehicle---
with tab3:
    with st.form("addVehicle", clear_on_submit=True):
        make = st.text_input("Please enter the vehicle make: ", key="make")
        model = st.text_input("Please enter the vehicle model: ", key="model")
        year = st.number_input("Please enter the vehicle year: ", key="year", value=0)
        submit = st.form_submit_button("submit")
        if submit:
            if vehicles.count_documents({'model': model}) != 0:
                st.exception("Vehicle already exists!")
            else:
                vehicles.insert_one({"make": make, "model": model, "year": year})
                st.success("Vehicle submitted")
                time.sleep(1)
                st.experimental_rerun()
# ---Remove Vehicle---
with tab4:
    with st.form("removeVehicle", clear_on_submit=True):
        vehicleRemove = st.selectbox(
            "Select a vehicle to add a record: ", selection, label_visibility="visible"
        )
        if st.form_submit_button("Remove"):
            vehicles.delete_many({"model": vehicleRemove})
            records.delete_many({"model": vehicleRemove})
            st.success(f"{vehicleRemove} removed successfully")
            time.sleep(1)
            st.experimental_rerun()
# ---Edit/remove record---
