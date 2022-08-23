#!/usr/bin/python3

# Automated pulling and compare to last known IP's for office 365 endpoints
# Created Feb 2019
# Tim Bowers, PCMS Group


import json
import os
import urllib.request
import uuid
from shutil import copyfile
import difflib


# helper to call the webservice and parse the response
def webApiGet(methodName, instanceName, clientRequestId):
    ws = "https://endpoints.office.com"
    requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
    request = urllib.request.Request(requestPath)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())

# path where client ID and latest version number will be stored
datapath = '/home/tim/scripts/endpoints_clientid_latestversion.txt'

# path where endpoints are stored
endpoint_path = '/home/tim/scripts/endpoints.txt'

# where old endpoints are stored for comparison
endpointold_path = '/home/tim/scripts/endpoints_old.txt'

# fetch client ID and version if data exists; otherwise create new file

if os.path.exists(datapath):
    with open(datapath, 'r') as fin:
        clientRequestId = fin.readline().strip()
        latestVersion = fin.readline().strip()
else:
    clientRequestId = str(uuid.uuid4())
    latestVersion = '0000000000'
    with open(datapath, 'w') as fout:
        fout.write(clientRequestId + '\n' + latestVersion)
# call version method to check the latest version, and pull new data if version number is different
version = webApiGet('version', 'Worldwide', clientRequestId)
if version['latest'] > latestVersion:
    print('New version of Office 365 worldwide commercial service instance endpoints detected')

    # move existing endpoints to 'old' file
    copyfile(endpoint_path,endpointold_path)

    # write the new version number to the data file
    with open(datapath, 'w') as fout:
        fout.write(clientRequestId + '\n' + version['latest'])
    # invoke endpoints method to get the new data
    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)
    # filter results for Allow and Optimize endpoints, and transform these into tuples with port and category
    flatUrls = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            category = endpointSet['category']
            urls = endpointSet['urls'] if 'urls' in endpointSet else []
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])
    flatIps = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            ips = endpointSet['ips'] if 'ips' in endpointSet else []
            category = endpointSet['category']
            # IPv4 strings have dots while IPv6 strings have colons
            ip4s = [ip for ip in ips if '.' in ip]
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])
    #print('IPv4 Firewall IP Address Ranges')
    #print('\n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    #print('URLs for Proxy Server')
    #print('\n'.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))
    # write the new version number to the data file
    with open(endpoint_path, 'w') as fout1:
        fout1.write('IPv4 Firewall IP Address Ranges\n')
        fout1.write('\n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
        fout1.write('\nURLs for Proxy Server\n')
        fout1.write('\n'.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))


    # TODO send mail (e.g. with smtplib/email modules) with new endpoints data

    # call diff to show difference between endpoints.txt and endpoints_old.txt
    endpoints = open(endpoint_path).readlines()
    endpoints_old = open(endpointold_path).readlines()

    for line in difflib.unified_diff(endpoints_old, endpoints):
        print(line),

else:
    print('Office 365 worldwide commercial service instance endpoints are up-to-date')

