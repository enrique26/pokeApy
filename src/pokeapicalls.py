from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import HTTPException
from typing import Dict
import requests

from settingClass import baseurl, apiBerries

# get all berries
def get_all_berries( setOffset: int = 0, setlimit: int = 0) -> Dict:
    response = requests.get(rf'{baseurl}{apiBerries}?offset={setOffset}&limit={setlimit}', 'w')
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch berry data")
    
# Function to get berry data from URL
def get_berry_data(url: str) -> Dict:
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch spacific berry data")