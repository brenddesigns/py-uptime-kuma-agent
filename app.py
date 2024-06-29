import requests
import time
import json
import threading
import os
from uptime_kuma_api import UptimeKumaApi, MonitorType
import ping3  # Importing ping3 for ICMP ping operations

# Static variables for Uptime Kuma instance
uptime_kuma_instance = [
    {
        "hostname": os.getenv('UPTIME_KUMA_INSTANCE_HOSTNAME'),
        "url": os.getenv('UPTIME_KUMA_INSTANCE_URL'),
        "username": os.getenv('UPTIME_KUMA_INSTANCE_USERNAME'),
        "password": os.getenv('UPTIME_KUMA_INSTANCE_PASSWORD')
    }
]
hosts = []

# Function to fetch hosts from Uptime Kuma instance
def fetch_monitors_from_kuma(api_url, username, password):
    fetched_hosts = []
    try:
        with UptimeKumaApi(api_url) as api:
            api.login(username, password)
            monitors = api.get_monitors()
            for monitor in monitors:
                if monitor['type'] == MonitorType.PUSH:
                    push_token = monitor['pushToken']
                    push_url = f"{api_url}/api/push/{push_token}?status=up&msg=OK&ping=<ping>"
                    hostname = monitor.get('description', "unknown")
                    fetched_hosts.append({
                        "name": monitor['name'],
                        "hostname": hostname,
                        "kuma_push_url": push_url,
                        "heartbeat_interval": monitor['interval']
                    })
    except Exception as e:
        print(f"Failed to fetch hosts from Uptime Kuma: {e}")
    return fetched_hosts

# Function to fetch hosts from Uptime Kuma instance and update config periodically
def fetch_monitors_periodically(api_url, username, password):
    while True:
        global hosts
        hosts = fetch_monitors_from_kuma(api_url, username, password)
        print("Updated hosts from Uptime Kuma instance.")
        time.sleep(60)  # Fetch hosts every 60 seconds

# Function to push the ping result to Kuma
def push_to_kuma(url, ping_value):
    """ Sends a push request to the Kuma URL with the ping time """
    try:
        push_url = url.replace("<ping>", str(ping_value))
        response = requests.get(push_url)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Failed to push to Kuma: {e}")
        return False

# Function to monitor all hosts respecting their respective heartbeat_interval
def monitor_all_hosts():
    while True:
        for host in hosts:
            internal_ping = ping3.ping(host["hostname"], unit='ms')
            if internal_ping is not None:
                for kuma_host in uptime_kuma_instance:
                    external_ping = round(ping3.ping(kuma_host["hostname"].replace("https://", "").replace("http://", ""), unit='ms'))
                    if external_ping is not None:
                        success = push_to_kuma(host["kuma_push_url"], external_ping)
                        if success:
                            print(f"Successfully pushed status for {host['name']}")
                        else:
                            print(f"Failed to push status for {host['name']}")
                        break  # Exit the loop once successful ping and push
                    else:
                        print(f"Failed to ping external Kuma instance for {host['name']}")
            else:
                print(f"Host {host['name']} is unreachable")
        
        # Determine the next sleep interval based on the shortest heartbeat_interval
        next_check = min(host["heartbeat_interval"] for host in hosts) if hosts else 30
        time.sleep(next_check)

if __name__ == "__main__":
    # Start a thread to periodically fetch hosts
    for kuma_host in uptime_kuma_instance:
        api_url = kuma_host['url']
        username = kuma_host['username']
        password = kuma_host['password']
        hosts = fetch_monitors_from_kuma(api_url, username, password)
        threading.Thread(target=fetch_monitors_periodically, args=(api_url, username, password)).start()

    # Start monitoring all hosts in the main thread
    monitor_all_hosts()