'''
Created by Alexei Rybalko aka Aagern.
'''

import requests, json, base64, logging, sys
from dataclasses import dataclass
from pprint import pprint

logging.basicConfig(filename="DeviceControl.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

@dataclass
class DeviceControl:
    API_URL: str = 'https://mdm.example.local'
    API_Key: str = 'oxGI6OORljw/Qsql1OFBycjHvzQzEXVXa/tyEcCfIPI='
    API_User: str = 'defaultDomain\\api_user:VMware1!'
    Serials_File: str = 'S.csv'
    Output_File: str = 'DeviceSerials.csv'    
    
    API_User_B64 = base64.b64encode(API_User.encode('utf-8'))  # convert to Base64
    API_User_UTF8 = API_User_B64.decode('utf-8')
    Platforms = {'Windows':12,'Linux':21}
    Header = {"Authorization": "Basic " + API_User_UTF8, "aw-tenant-code": API_Key, "Accept": "application/json"}
    Devices = {}
    Serials = []
    
    def getMDM(self,request):
        """Get data from MDM Server. Input: API request text. Output: response data in JSON."""
        try:
            dataMDM = requests.get(self.API_URL + request, headers=self.Header)
            dataMDM.raise_for_status()
            data = dict(dataMDM.json())
        except requests.exceptions.RequestException as e:
            logging.error(f'Get request failed with {e}')
            sys.exit(1)
        logging.debug(f'Data received from {self.API_URL}')
        return data
        
    def postMDM(self,request,data):
        """Post data to MDM Server. Input: API request text. Output: HTTP response status and details."""
        try:
            responseMDM = requests.post(self.API_URL + request, headers=self.Header, json=data) # Important to do json= here, rather than prepare data with json.dumps()
        except requests.exceptions.RequestException as e:
            logging.error(f'Post request failed with {e}')
            sys.exit(1)
        logging.debug(f'Data sent to {self.API_URL}')        
        return responseMDM
    
    def scanSerialsFile(self,file=Serials_File):
        """Input file with device serials. Output list of serials from file"""
        try:
            with open(file,encoding='utf-8') as f:
                for serial_line in f:
                    self.Serials.append(serial_line)
                    Serials[0] = Serials[0][1:] # Omitting special symbol at file start
                logging.debug(f'Serials file {file} processed.')
        except OSError as e:
            logging.error(f'File opening error with {e}')
            print('File not opened. Serials list empty')
            self.Serials = []
        return self.Serials
            
    def filterDevices(self,platform='Windows'):
        """
        Method filters out Devices by Platform. 
        Inputs: Platform name. 
        Outputs: File with serials, Dictionary of Device:[Serial,ID]
        """
        PlatformID = self.Platforms[platform]
        dataDict = self.getMDM('/api/mdm/devices/search')
        for device in dataDict['Devices']:
            if device['PlatformId']['Id']['Value'] == PlatformID:
                self.Devices[device['DeviceFriendlyName']] = [device['SerialNumber'] if device['SerialNumber'] else 'Not set',device['Id']['Value']]
        try:
            with open(self.Output_File,mode="wt",encoding='utf-8') as output_file:
                for device,serial in self.Devices.items():
                    print(f"{device},{serial},",file=output_file)
                    if serial in Serials: print("Registered\n",file=output_file)
                    else: print("NOT Registered\n",file=output_file)
                logging.debug(f'Output file {self.Output_File} written.')
        except OSError as e:
            logging.error(f'File opening error with {e}')
            print('File not written.')
            sys.exit(1)
        return self.Devices
    
    def getMDMTags(self,tenant='570'):
        """Get all tags in tenant. Input: tenant ID. Output: list of tags and their IDs."""
        tagsDict = self.getMDM(f'/api/system/groups/{tenant}/tags')
        for tag in tagsDict['Tags']:
            print(f"Name={tag['TagName']}\t\tID={tag['Id']}")
            
    def setTagDevices(self,tagID='10000',DeviceIDs=['3']):
        """Method assigns devices to tag. Input: tag id, devices ID list. Output: total  of assigned devices""" 
        FuncDeviceIDs = { "BulkValues":{"Value":DeviceIDs}}
        response = self.postMDM(f'/api/mdm/tags/{tagID}/adddevices',FuncDeviceIDs)
        print(f'Status code: {response.status_code}, \n {response.text}')

# Usage Examples:
        
Device = DeviceControl()
data = Device.filterDevices()
Device.getMDMTags()
Device.setTagDevices()
pprint(data)
