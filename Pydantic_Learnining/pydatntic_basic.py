from pydantic import BaseModel


#Created Pydantic Class for validation
class Patient(BaseModel):
    name : str
    age  : int
    

#Now we are getting patient object of type Patient   
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Patient info is inserted")
    
    
patient_info = {"name":"gulam", "age":25}

#Intantiate Pydantic object for validation
patient1 = Patient(**patient_info)

#Now insert data with the help of patient_object

insert_patient_data(patient1)