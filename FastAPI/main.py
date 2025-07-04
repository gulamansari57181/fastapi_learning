# importing FASTAPI Class

from fastapi import FastAPI, HTTPException, Path ,Query
import json ,os

app= FastAPI()

# To load our patient data

def load_data():
   try:
        if not os.path.exists("patient.json"):
            raise FileNotFoundError("patient.json file not found.")

        with open("patient.json", 'r') as f:
            data = json.load(f)
        
        return data
    
   except json.JSONDecodeError as e:
         raise ValueError("Invalid JSON format in patient.json")

# Decorator
@app.get("/") 
# Method
def hello():
        return {"message":" This is patient management system api."}
 
#To craete another endpoint : about
@app.get("/about")

def about():
    return {"message":"Welocme to fully functional API to manage your patient records."} 



@app.get("/view")

def view():
    # Loading and return patient data as http response
    data = load_data()
    return data
    

# To view specific patient details

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(...,description="ID of the patient in the database", example="P001")):
    # We will load all the patient data here and then find specific patien
    
        data = load_data()

        if patient_id in data:
            return data[patient_id]
        else:
            raise HTTPException(status_code=404, detail="Patient not found")
    
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort patients by height, weight, or bmi"),
    order: str = Query('asc', description="Sort order: asc or desc")
):

    valid_fields = ["height" , "weight", "bmi"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400 , detail= f"Invalid feild, select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException (status_code =400 , detail= "Invalid order choose from asc or desc")

    sort_order = True if order=='desc' else False
    
    # To sort the data as per above query
    data = load_data()
    
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse = sort_order)
    
    return sorted_data
    
        
    
    
    
# Command to run : uvicorn filename:appname --reload