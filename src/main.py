
from typing import List, Dict
import requests
import concurrent.futures
from fastapi import FastAPI, HTTPException
from pokeapicalls import get_all_berries;
from concurrent.futures import ThreadPoolExecutor

from settingClass import baseurl,apiBerries, offsetBerries, limitBerries

app = FastAPI()


# Function to get all berry data from pokeapi
def get_berry_data(url: str) -> Dict:
    response = requests.get(url)
    if response.status_code == 200:
        #print(response.json())
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch berry data")

growth_times = []
berries_names = []
# Function to get each berry stats
def get_berry_stats_call(berry_urls: List[str]) -> Dict:
    id_berry = berry_urls["url"].split('/')[-2]
    #gettin the data for each berry and store the growth_time
    berry_data = get_berry_data(rf'{baseurl}{apiBerries}{id_berry}')
    growth_time = berry_data.get("growth_time")
    #check if the json has "growth_time" field
    if growth_time:
        growth_times.append(growth_time)
        berries_names.append(berry_data.get("name"))
        return berry_data
    if not growth_times:
        raise HTTPException(status_code=404, detail="No growth time data found")


def calculate_stats() -> Dict:
    # Calculating statistics after get all the berries data
    min_growth_time = min(growth_times)
    median_growth_time = sorted(growth_times)[len(growth_times) // 2]
    max_growth_time = max(growth_times)
    variance_growth_time = sum((x - sum(growth_times) / len(growth_times)) ** 2 for x in growth_times) / len(growth_times)
    mean_growth_time = sum(growth_times) / len(growth_times)
    frequency_growth_time = {time: growth_times.count(time) for time in set(growth_times)}

    return {
        "berries_names": berries_names,
        "min_growth_time": min_growth_time,
        "median_growth_time": median_growth_time,
        "max_growth_time": max_growth_time,
        "variance_growth_time": variance_growth_time,
        "mean_growth_time": mean_growth_time,
        "frequency_growth_time": frequency_growth_time
    }

#endpoint get allBerryStats
@app.get("/allBerryStats")
def allBerryStats():
    getallBerries = get_all_berries(offsetBerries, limitBerries)

    # Create a ThreadPoolExecutor to perform async calls to get the information for each berry
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit each URL for fetching data getallBerries[results]
        future_to_url = {executor.submit(get_berry_stats_call, url): url for url in getallBerries['results']}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as e:
                print(f"Error fetching data from {e}")
            else:
                print(data)

    return calculate_stats() 