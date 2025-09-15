import streamlit as st
import requests

API_URL = "https://patient-api-zo4v.onrender.com"

st.set_page_config(page_title="Patient Management Dashboard", layout="centered")
st.title("👩‍⚕️ Patient Management Dashboard")

# Navigation Sidebar
menu = st.sidebar.radio("📁 Menu", ["Home", "View All", "View by ID", "Add Patient", "Edit Patient", "Delete Patient", "Sort Patients"])

# 1. Home
if menu == "Home":
    try:
        res = requests.get(f"{API_URL}/")
        if res.status_code == 200:
            st.success(res.json()["message"])
        else:
            st.error("API not reachable.")
    except Exception as e:
        st.error(f"Error: {e}")

# 2. View All Patients
elif menu == "View All":
    st.subheader("🔄 All Patients")
    res = requests.get(f"{API_URL}/view")
    if res.status_code == 200:
        patients = res.json()
        for pid, info in patients.items():
            with st.expander(f"🩺 {info['name']} (ID: {pid})"):
                st.json(info)
    else:
        st.error("Could not fetch patient data.")

# 3. View by ID
elif menu == "View by ID":
    st.subheader("Search by Patient ID")
    pid = st.text_input("Enter Patient ID")
    if st.button("Search"):
        res = requests.get(f"{API_URL}/patient/{pid}")
        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error("Patient not found.")

# 4. Add Patient
elif menu == "Add Patient":
    st.subheader("Add New Patient")
    with st.form("add_form"):
        pid = st.text_input("Patient ID")
        name = st.text_input("Name")
        city = st.text_input("City")
        age = st.number_input("Age", 1, 120)
        gender = st.selectbox("Gender", ["male", "female", "others"])
        height = st.number_input("Height (m)", 0.5, 2.5)
        weight = st.number_input("Weight (kg)", 10.0, 200.0)
        submitted = st.form_submit_button("Create")
        if submitted:
            payload = {
                "id": pid,
                "name": name,
                "city": city,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight
            }
            r = requests.post(f"{API_URL}/create", json=payload)
            if r.status_code == 201:
                st.success("Patient created successfully.")
            else:
                st.error(r.json().get("detail", "Failed to create patient."))

# 5. Edit Patient
elif menu == "Edit Patient":
    st.subheader("Edit Patient Info")
    pid = st.text_input("Enter Patient ID to Edit")
    if st.button("Fetch Current Data"):
        res = requests.get(f"{API_URL}/patient/{pid}")
        if res.status_code == 200:
            pdata = res.json()
            with st.form("edit_form"):
                name = st.text_input("Name", value=pdata["name"])
                city = st.text_input("City", value=pdata["city"])
                age = st.number_input("Age", 1, 120, value=pdata["age"])
                gender = st.selectbox("Gender", ["male", "female"], index=["male", "female"].index(pdata["gender"]))
                height = st.number_input("Height (m)", 0.5, 2.5, value=pdata["height"])
                weight = st.number_input("Weight (kg)", 10.0, 200.0, value=pdata["weight"])
                submitted = st.form_submit_button("Update")
                if submitted:
                    update_payload = {
                        "name": name,
                        "city": city,
                        "age": age,
                        "gender": gender,
                        "height": height,
                        "weight": weight
                    }
                    r = requests.put(f"{API_URL}/edit/{pid}", json=update_payload)
                    if r.status_code == 200:
                        st.success("Patient updated successfully.")
                    else:
                        st.error(r.json().get("detail", "Update failed."))
        else:
            st.error("Patient not found.")

# 6. Delete Patient
elif menu == "Delete Patient":
    st.subheader("🗑️Delete Patient Record")
    pid = st.text_input("Enter Patient ID to Delete")
    if st.button("Delete"):
        r = requests.delete(f"{API_URL}/delete/{pid}")
        if r.status_code == 200:
            st.success("Patient deleted.")
        else:
            st.error(r.json().get("detail", "Deletion failed."))

# 7. Sort Patients
elif menu == "Sort Patients":
    st.subheader("Sort Patient Records")
    sort_by = st.selectbox("Sort by", ["height", "weight", "bmi"])
    order = st.radio("Order", ["asc", "desc"])
    if st.button("Sort"):
        try:
            res = requests.get(f"{API_URL}/sort?sort_by={sort_by}&order={order}")
            if res.status_code == 200:
                sorted_data = res.json()
                for patient in sorted_data:
                    with st.expander(f"{patient['name']}"):
                        st.json(patient)
            else:
                st.error("Sorting failed.")
        except Exception as e:
            st.error(f"Error: {e}")
