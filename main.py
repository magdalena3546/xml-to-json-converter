from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Annotated
import xml.etree.ElementTree as ET
from script import parse_xml, create_json, DuplicateEmployee
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/files")
async def create_json_file(file: UploadFile = File(...)):
    try:
        root = await parse_xml(file)
        create_json(root)
        logging.info("Json file created successfully.")
        return {"message": "File parse successfully"}
    except ET.ParseError:
        logging.info("Invalid xml file.")
        raise HTTPException(status_code=400, detail="This file is not valid xml file.")
    except DuplicateEmployee as e:
        logging.info("Duplicate employee.")
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logging.info("Unexpected error occurred.")
        raise HTTPException(status_code=500, detail=f"An error: {str(e)}")

