from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from pathlib import Path

# Initializing the application server.
app = FastAPI()

# Defining class models (structs).
class Files(BaseModel):
    id: str
    name: str
    meta: Dict[str, Any]

class Response(BaseModel):
    operationType: str
    count: int
    objects: List[Dict[str, Any]]

class SyncTwoDates_Response(BaseModel):
    message: str
    operations: List[Response]

# Function use for loading JSONL files into variables.
def load_files(path: str) -> List[Files]:
    file_path = f"dms-responses/{path}.jsonl"

    if not Path(file_path).exists():
        raise HTTPException(status_code = 404, detail = f"{file_path} >> File Not Found")
    
    try:
        with open(file_path, "r") as file:
            return [Files(**json.loads(line)) for line in file]
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"An error occurred >> Executing Load Files Function : {str(e)}")

# Function use in order to search create operations between two dates.
def search_create_ops(start_dict: Dict[str, Files], end_dict: Dict[str, Files]) -> List[Response]:
    result = []
    operations = []
    
    for file_id, file in end_dict.items():
        if file_id not in start_dict:
            operations.append({"file": file.model_dump()})

    result.append({"operationType": "Create Files Operations", "count": len(operations), "objects": operations})

    return result

# Exposing GET endpoint that compares two dates.
@app.get("/syncTwoDates")
def sync_files_two_dates(start_date: str, end_date: str) -> SyncTwoDates_Response:
    start_files = load_files(start_date)
    end_files = load_files(end_date)

    start_dict = {file.id: file for file in start_files}
    end_dict = {file.id: file for file in end_files}
    
    operations = search_create_ops(start_dict, end_dict)

    return {"message": f"Operations made from {start_date} to {end_date}.","operations": operations}
