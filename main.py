import os
import json
import socket
import ssl

import shodan
from dotenv import load_dotenv
from tqdm import tqdm


def load_shodan_api_key():
    """Load the Shodan API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        raise ValueError("SHODAN_API_KEY not found in .env file")
    return api_key


def cert_is_valid(hostname, port, timeout=3):
    """Check if the SSL certificate for the given hostname and port is valid."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
                return True
    except Exception:
        return False


def search_derp_nodes(api, query, limit=500):
    """Search Shodan for DERP nodes matching the query."""
    results = api.search(query, limit=limit)
    nodes = []

    matches = results.get("matches", [])
    for result in tqdm(matches, desc="Processing DERP nodes"):
        hostnames = result.get("hostnames", [])
        if not hostnames:
            continue
        ip = result.get("ip_str")
        port = result.get("port")
        hostname = hostnames[0]
        node = {
            "Name": f"{ip}:{port}",
            "RegionID": 900,
            "DERPPort": port,
            "HostName": hostname,
        }
        if "derp" in hostname and cert_is_valid(hostname, port):
            nodes.append(node)
    return nodes


def deduplicate_and_sort_nodes(nodes):
    """Deduplicate nodes by HostName and sort them by HostName."""
    unique_nodes = {}
    for node in nodes:
        key = node["HostName"]
        if key not in unique_nodes:
            unique_nodes[key] = node
    sorted_nodes = sorted(unique_nodes.values(), key=lambda n: n["HostName"])
    return sorted_nodes


def save_nodes_to_file(nodes, filename="derp.json"):
    """Save the list of nodes to a JSON file."""
    with open(filename, "w") as f:
        json.dump({"Nodes": nodes}, f, indent=2)


def main():
    api_key = load_shodan_api_key()
    api = shodan.Shodan(api_key)
    query = 'has_ssl:true http.html:"DERP server" country:"HK"'
    nodes = search_derp_nodes(api, query)
    sorted_nodes = deduplicate_and_sort_nodes(nodes)
    save_nodes_to_file(sorted_nodes)


if __name__ == "__main__":
    main()
