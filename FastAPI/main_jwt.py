# importing FASTAPI Class

from fastapi import FastAPI, Path, HTTPException, Query , Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json , os

#Import module for jwt authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import create_access_token, get_password_hash, verify_password, decode_token

#Adding dummy user database
users_db = {
    "admin": {
        "username": "admin",
        "full_name": "System Admin",
        "hashed_password": get_password_hash("adminpass")
    }
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app= FastAPI()


# Creating Pydatic Data Model which will be useful for data validation and constraint restriction

class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]
    
    
    #To create a new computed field (bmi) from exisiting field by  weight and height
    @computed_field
    @property

    def bmi(self)-> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    #Also we have to comment on verdict based on the bmi of the patient
    #This is achieve by computed_field functionality provided by pydantic
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
        

#To tackle update patient detials , we have to create another pydantic object
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
    
#Login BaseModel
class LoginModel(BaseModel):
    username: str
    password: str

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
     
     
     
#To save new data of patient into our database

def save_data(data):
    #We are getting python dictionary as an input
    #we have to dump it into json file
    with open("patient.json","w") as f:
        json.dump(data, f)
        

#To implement authorization dependancy      
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["sub"]

        
        

#From here onwatds we are creating our endpoints

# Decorator
 #To craete another endpoint : about
@app.get("/")

def about():
    return {"message":"Welcome to fully functional API to manage your patient records."} 



@app.get("/view", dependencies=[Depends(get_current_user)])

def view():
    # Loading and return patient data as http response
    data = load_data()
    return data
    

# To view specific patient details
@app.get("/patient/{patient_id}", response_model=Patient, dependencies=[Depends(get_current_user)])


def view_patient(patient_id:str = Path(...,description="ID of the patient in the database", example="P001")):
    # We will load all the patient data here and then find specific patient
    
        data = load_data()

        if patient_id in data:
            patient_info = data[patient_id]
            # Reattaching the 'id' field before returning
            patient_info['id'] = patient_id
            return patient_info
        else:
            raise HTTPException(status_code=404, detail="Patient not found")
 
 
    
@app.get("/sort", dependencies=[Depends(get_current_user)])
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

@app.post(r"/create", dependencies=[Depends(get_current_user)])
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
    
  
# To create update and delete endpoints

@app.put('/edit/{patient_id}', dependencies=[Depends(get_current_user)])
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete(r'/delete/{patient_id}', dependencies=[Depends(get_current_user)])
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})


#To implement login auth
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

  
    
# To launch server I am using this command : uvicorn filename:appname --reload