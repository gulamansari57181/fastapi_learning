# importing FASTAPI Class

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json , os

# importing pydantic

from pydantic import BaseModel , Field
from typing import   Annotated 
app= FastAPI()


# Creating Pydatic Data Model 

class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]
    
    
    #To create a new computed field (bmi) from exisiting field such as weight and height
    @computed_field
    @property

    def bmi(self)-> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    #Also we have to comment on verdict based on the bmi of the patient
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        

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
     
     
     
#To save new data of patient into our json file

def save_data(data):
    #We are getting python dictionary as an input
    #we have to dump it into json file
    with open("patient.json","w") as f:
        json.dump(data, f)
        
        

#From here onwatds we are creating our endpoints

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
    # We will load all the patient data here and then find specific patient
    
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
    

# endpoint to add patient details into the database after pydantiv validation

@app.post(f"/create")
def create_patient(patient: Patient):

    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})     
    
    
    
# Command to run : uvicorn filename:appname --reload