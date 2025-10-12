from fastapi import FastAPI, HTTPException
import datetime
import os
import json
from fastapi.middleware.cors import CORSMiddleware

#TODO: put it in a constants file
ROOT_DIR=os.path.abspath(os.curdir)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - only for development!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"Ping": "Pong"}


@app.get("/challenge/{date}")
def read_challenge(date: str):
    try:
        datetime.datetime.strptime(date,"%Y-%m-%d").date()
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")
    
    file_path = ROOT_DIR + "/challenges/" + date + ".json"
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Challenge does not exist!")
        
    try:
        with open(file_path,'r') as challenge_file:
            return json.load(challenge_file)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Challenge file is corrupted")
    except IOError:
        raise HTTPException(status_code=500, detail="Could not read challenge file")
            
        
    