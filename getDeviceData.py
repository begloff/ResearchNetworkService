import sys
import os
import subprocess
import json
from datetime import datetime

def getDeviceData(dt, dirname):   
    #runs a process to get information about the current network connection
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode()

    output = results.split('\n')
    currConnection = {}
    data = {}

    #parses the data and gets various categories
    #more categorires can be added to this section in the future
    #if more data is required as not all are parsed out
    for line in output:
        line = line.strip()
        key = line.split(':')
        key[0] = key[0].strip()
        if key[0] == 'BSSID':
            tempkey = key[1:]
            tempkey = ':'.join(tempkey)
            key = ['BSSID', tempkey]
        elif key[0] == 'Physical address':
            tempkey = key[1:]
            tempkey = ':'.join(tempkey)
            key = ['Physical address', tempkey.strip()]
        elif key[0] == 'Signal':
            signal = key[1][1:-1]
            signal = int(signal)
            rssi = (signal/2) - 100
            data['RSSI'] = rssi
            continue
        if len(key[0]):
            if len(key[1]):
                key[1] = key[1].strip()
                data[key[0]] = key[1]


    #runs a process to see available networks and physical connections
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=bssid']).decode()
    output = results.split('\n')

    #parses data from all available networks command\
    #separates data by SSID and then by BSSID under the ssid
    linenum = 0
    currid = ''
    processbid = False
    ssids = {}
    for line in output:
        if line[:4] == 'SSID':
            currid = line.split(':')[1].strip()
            ssids[currid] = {} #dictionary of BSSIDs for each SSID
            processbid = False
            continue
        if not len(ssids):
            continue
        line = line.strip()
        if 'BSSID' in line:
            bid = line.split(':')
            bid = ':'.join(bid[1:]).strip()
            ssids[currid][bid] = {} #dictionary of attributes for each BSSID
            processbid = True
            continue
        if not processbid:
            continue
        #Can add sections to here to parse more data from each BSSID
        #
        #
        #
        if 'Signal' in line:
            signal = line.split(':')[1].strip()[:-1]
            signal = int(signal)
            rssi = (signal/2) - 100
            ssids[currid][bid]['RSSI'] = rssi
            ssids[currid][bid]['Signal'] = signal
        if 'Band'in line:
            band = line.split(':')[1].strip()
            ssids[currid][bid]['Band'] = band
        if 'Channel' in line and 'Utilization' not in line:
            channel = line.split(':')[1].strip()
            ssids[currid][bid]['Channel'] = channel
        elif 'Channel' in line:
            channel = line.split(':')[1].strip()
            ssids[currid][bid]['Utilization'] = channel

    #adds data to the current network connection section of the json file
    currConnection = ssids[data['SSID']][data['BSSID']]
    currConnection['SSID'] = data['SSID']
    currConnection['BSSID'] = data['BSSID']
    currConnection['Receive rate (Mbps)'] = data['Receive rate (Mbps)']
    currConnection['Transmit rate (Mbps)'] = data['Transmit rate (Mbps)']         

    jsonDump = {'Current Connection': currConnection, 'All Connections': ssids}

    heatCount = 0
    for key in jsonDump['All Connections']:
        count = 0
        for addr in ssids[key]:
            count += 1
            if key == currConnection['SSID']:
                heatCount+=1
    
    #-returns the number of availble connections on the current networ
    return jsonDump