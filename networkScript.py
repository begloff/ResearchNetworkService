import subprocess
import json
import speedtest
from getDeviceData import getDeviceData
import requests
import uuid

def get_ip():
    
    #FETCH IP ADDRESS OF CALLING DEVICE    
    
    try:
        result = subprocess.run(['curl', 'ifconfig.me'], capture_output=True, text=True, timeout=5)
        ip_address = result.stdout.strip()
        return ip_address
    except subprocess.TimeoutExpired:
        print("Curl command timed out.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Curl command failed with error: {e}")
        return None

def run_speed_test():
    
    # RUN SPEEDTEST FOR CALLING DEVICE
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1e6
    upload_speed = st.upload() / 1e6
    
    # Can take a while to get up & down
    return {"download_speed": download_speed, "upload_speed": upload_speed}

def get_mac_address():
    
    # Fetch mac address of calling device
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac_address[i:i+2] for i in range(0, 12, 2)])

if __name__ == "__main__":
    # COMPILE DATA FROM CALLING DEVICE
    
    ip_data = {}

    #IP ADDRESS
    ip = get_ip()
    if ip:
        ip_data["ip_address"] = ip
        
    #MAC ADDRESS
    mac_address = get_mac_address()
    if mac_address:
        ip_data["mac_address"] = mac_address

    #SPEED TEST
    speed_test_data = run_speed_test()
    ip_data.update(speed_test_data)
    
    #FETCH WIFI NEIGHBORHOOD DATA AND MORE SPECIFIC CONNECTION DATA
    deviceData = getDeviceData(None, None)
    ip_data.update(deviceData)
    
    
    
    #DATA IS COMPILED: EXECUTE METHODS TO DELIVER DATA
    
    
    #1. Print data to log file
    print(f'OUTPUT: {json.dumps(ip_data, indent=4)}')
    
    #2. Post Data to API --> must run express server locally first
    url = "http://localhost:3000/api/v1/networkinfo"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(ip_data), headers=headers)
    
    if response.status_code == 200:
        print("POST request successful.")
    else:
        print(f"POST request failed with status code {response.status_code}.")
        
        
    #Can modify post request based on further api expansion or if something more permanent is established
