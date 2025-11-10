from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from requests.auth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

JAMF_BASE_URL = os.getenv("JAMF_BASE_URL", "https://vajiravudh.jamfcloud.com/JSSResource")
JAMF_USERNAME = os.getenv("JAMF_USERNAME")
JAMF_API_KEY = os.getenv("JAMF_API_KEY")

@app.get("/")
def root():
    return {"message": "Jamf backend is running"}

@app.get("/api/device")
def get_device(search: str = Query(..., description="Device name to search for")):
    try:
        response = requests.get(
            f"{JAMF_BASE_URL}/devices?name={search}",
            auth=HTTPBasicAuth(JAMF_USERNAME, JAMF_API_KEY)
        )

        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content={
                "error": f"JAMF API request failed with {response.status_code}"
            })

        data = response.json()
        devices = data.get("devices", [])
        if not devices:
            return {"message": "No devices found"}

        return devices[0]

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/api/serial")
def get_device_serial(serial: str = Query(..., description="Serial number to search for")):
    try:
        response = requests.get(
            f"{JAMF_BASE_URL}/devices?serialnumber={serial}",
            auth=HTTPBasicAuth(JAMF_USERNAME, JAMF_API_KEY)
        )

        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content={
                "error": f"JAMF API request failed with {response.status_code}"
            })

        data = response.json()
        devices = data.get("devices", [])
        if not devices:
            return {"message": "No devices found"}

        return devices[0]

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})