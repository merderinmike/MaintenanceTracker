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
    def clearCheck():
        st.session_state["Tasks"] = False
        st.session_state["Miles"] = False
        st.session_state["Parts"] = False
        st.session_state["Cost"] = False


    recordselect = st.selectbox(
        "Select a vehicle to view record", selection)
    "---"
    x = []
    findRecord = list(records.find({'model': recordselect}, {"_id": 0}))
    for entry in findRecord:
        x.append(entry)
    df = pd.DataFrame(x)
    if recordselect != selection[0]:
        st.table(df)
    action = st.selectbox("Edit or Remove a record?", ["Make Selection", "Edit", "Remove"])
    if action == "Edit":
        lst = []
        findRecord = list(records.find({'model': recordselect}, {"_id": 0}))
        for x in findRecord:
            lst.append(x)
        recordEdit = st.selectbox("Select your record", [lst[0]['tasks']])
        checks = st.columns(4)
        button1, button2 = st.columns(2)
        with checks[0]:
            checkTasks = st.checkbox("Tasks", key="Tasks")
        with checks[1]:
            checkMiles = st.checkbox("Miles", key="Miles")
        with checks[2]:
            checkParts = st.checkbox("Parts", key="Parts")
        with checks[3]:
            checkCost = st.checkbox("Cost", key="Cost")
        with st.form("Edit"):
            if checkTasks:
                tasks = st.text_area("Tasks", placeholder="What tasks were performed? ", key="tasks1")
            else:
                tasks = lst[0]['tasks']
            if checkMiles:
                miles = str(st.number_input("Enter miles of vehicle", key="miles1", value=0, ))
            else:
                miles = lst[0]['miles']
            if checkParts:
                parts = st.text_area("Enter what parts were used for this task (If none leave blank)", key="parts1")
            else:
                parts = lst[0]['parts']
            if checkCost:
                cost = st.number_input("Enter total cost of task (Include any tools needed to complete task)",
                                       key="cost1",
                                       value=0,
                                       min_value=0)
            else:
                cost = lst[0]['cost']
            if st.form_submit_button("update"):
                records.update_many({"$and": [{"tasks": recordEdit}]},
                                    {"$set": {"miles": miles, "tasks": tasks, "parts": parts, "cost": cost}})
            if st.form_submit_button("Submit", on_click=clearCheck):
                st.experimental_rerun()

    elif action == "Remove":
        lst = []
        try:
            with st.form("Remove"):
                findRecord = list(records.find({'model': recordselect}, {"_id": 0}))
                for x in findRecord:
                    lst.append(x)
                recordRemove = st.selectbox("Select your record", [lst[0]['tasks']])


                def remove():
                    records.delete_one({"tasks": recordRemove})
                    st.experimental_rerun()


                st.form_submit_button("Submit", on_click=remove)

        except:
            st.error("There are no records for this vehicle to be removed")

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
            "Select a vehicle to remove: ", selection, label_visibility="visible"
        )
        if st.form_submit_button("Remove"):
            vehicles.delete_many({"model": vehicleRemove})
            records.delete_many({"model": vehicleRemove})
            st.success(f"{vehicleRemove} removed successfully")
            time.sleep(1)
            st.experimental_rerun()
