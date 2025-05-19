import json
import os

import shodan
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")

if not SHODAN_API_KEY:
    raise ValueError("SHODAN_API_KEY not found in .env file")

# print("Your Shodan API key is:", SHODAN_API_KEY)


api = shodan.Shodan(SHODAN_API_KEY)

# Search for DERP nodes (adjust the query as needed)
results = api.search('tailscale derp country:"US"', limit=100)

nodes = []
for result in results["matches"]:
    ip = result.get("ip_str")
    port = result.get("port")
    node = {
        "Name": f"{ip}:{port}",
        "RegionID": 900,
        "HostName": ip,
        "IPv4": ip,
        "DERPPort": port,
    }
    nodes.append(node)

with open("derp.json", "w") as f:
    json.dump({"Regions": {"900": {"Node": nodes}}}, f, indent=2)
