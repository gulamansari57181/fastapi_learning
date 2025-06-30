# importing FASTAPI Class

from fastapi import FastAPI

app= FastAPI()

# Decorator
@app.get("/") 
# Method
def hello():
        return {"Message":" created fist api endpoint!!!"}
    
# Command to run : uvicorn filename:appname --reload