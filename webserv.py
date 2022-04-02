from fastapi import FastAPI
from typing import Optional
from shodan import Shodan

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/ip/{ip}")
async def get_ip(ip: str, key: Optional[str] = None):
    if key is None:
        return {"Error": "Please provide a valid API key"}
    else:
        try:
            api = Shodan(key)
            res = api.host(ip)
            return {
                "IP": res["ip_str"],
                "Organization": res["org"],
                "Country": res["country_name"],
                "Region":res["region_code"],
                "City":res["city"],
                "Lat":res["latitude"],
                "Long":res["longitude"],
                
                "Lg":res,


            }
        except Exception as e:
            return {"Error": str(e)}