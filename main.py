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