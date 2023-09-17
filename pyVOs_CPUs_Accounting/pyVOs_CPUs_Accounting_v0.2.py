#!/usr/bin/env python3
#
#  Copyright 2023 EGI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Install requirements:
# ]$ sudo pip3 install gspread
# Credentials: python-google-sheet-service-ac@striped-rhino-395008.iam.gserviceaccount.com
# Google spread-sheet: https://docs.google.com/spreadsheets/d/1B1Sqf1UiN9pY_fGbWe5G1zKA2UzsekOVbLCtiiMFAXk/edit#

import datetime
import gspread
import json
import requests
import warnings
warnings.filterwarnings("ignore")
from utils import colourise, highlight, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.2"
__date__      = "$Date: 24/08/2023 10:50:22"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__   = "Apache Licence v2.0"


def connect(env):
    ''' Connecting to the EGI Accounting Portal '''
    
    _url = "%s/%s/%s/VO/DATE/%s/%s/%s/%s/%s/" %(env['ACCOUNTING_SERVER_URL'], 
            env['ACCOUNTING_SCOPE'],
            env['ACCOUNTING_METRIC'],
            env['DATE_FROM'], 
            env['DATE_TO'],
            env['ACCOUNTING_VO_GROUP_SELECTOR'],
            env['ACCOUNTING_LOCAL_JOB_SELECTOR'],
            env['ACCOUNTING_DATA_SELECTOR'])

    headers = { "Accept": "Application/json" }
    
    if env['LOG'] == "DEBUG":
        print(colourise("cyan", "\n[INFO]"), \
              "- Fetching accounting records from: %s" %env['ACCOUNTING_SERVER_URL'])
    
    curl = requests.get(url=_url, verify=True)
    data = curl.json()

    return data


def get_GWorkSheetCellPosition(worksheet, accounting_period):
    ''' Get the cell coordinates where to add the new reporting period '''

    _cell = _cell2 = ""
    flag = False

    for item in worksheet.get_all_records():
        cell = worksheet.find(item['Period'])
        if item['Period'] < accounting_period:
            _cell2 = cell.row
        else:
            _cell = cell
            flag = True
            break

    if not flag:
        return (_cell2+1)
    else:    
        return(_cell.row)
    

def update_GWorkSheet(env, accounting_period, total_cpu, noVOCPUs, totalVOCPUs):
    ''' Update the accounting records in the Google Worksheet '''

    # Get the service account
    account = gspread.service_account(env['SERVICE_ACCOUNT_FILE'])
    # Open the GoogleSheet
    sheet = account.open(env['GOOGLE_SHEET_NAME'])
    # Open the proper Worksheet based on the SCOPE
    if (env['ACCOUNTING_SCOPE'] == "cloud"):
       worksheet = sheet.worksheet(env['GOOGLE_CLOUD_WORKSHEET'])
    else:   
       worksheet = sheet.worksheet(env['GOOGLE_HTC_WORKSHEET'])

    # Formatting the header of the worksheet
    worksheet.format("A1:D1", {
      "backgroundColor": {
      "red": 55.0,
      "green": 15.0,
      "blue": 10.0
      },
      "horizontalAlignment": "LEFT",
      "textFormat": { "fontSize": 11, "bold": True }
    })

    # Formatting the cells of the worksheet
    worksheet.format("A2:D30", {
      "horizontalAlignment": "RIGHT",
      "textFormat": { "fontSize": 11 }
    })

    dt = datetime.datetime.now()
    # Convert dt to string in dd-mm-yyyy HH:MM:SS
    timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")

    flag = False # Accounting period not found in the GSpreadsheet
    for item in worksheet.get_all_records():
        if (item['Period'] == accounting_period):
           flag = True

           cell = worksheet.find(item['Period'])
           # Updating the cell of the Google Worksheet
           worksheet.update_cell(cell.row, cell.col + 1, total_cpu)
           worksheet.update_cell(cell.row, cell.col + 2, totalVOCPUs)
           worksheet.update_cell(cell.row, cell.col + 3, len(noVOCPUs))
           if len(noVOCPUs):
              worksheet.update_cell(cell.row, cell.col + 4, ', '.join([str (item) for item in noVOCPUs]))
           else:   
              worksheet.update_cell(cell.row, cell.col + 4, '-')

    if not flag:
           print("Adding %s" %accounting_period + " at row:", 
                   get_GWorkSheetCellPosition(worksheet, accounting_period))
           
           if len(noVOCPUs):
              body = [accounting_period, 
                      total_cpu, 
                      totalVOCPUs, 
                      len(noVOCPUs), 
                      ', '.join([str (item) for item in noVOCPUs])]

           else:
               body = [accounting_period,
                      total_cpu,
                      totalVOCPUs,
                      len(noVOCPUs),
                      '-']
           
           index = get_GWorkSheetCellPosition(worksheet, accounting_period)
           worksheet.insert_row(body, index=index)

    # Update the timestamp of the last update
    worksheet.update("G1","Last update on: " + timestamp)


def main():

    # Initialise environment variables
    total = total_noVOCPUs = total_cloud_cpu = total_htc_cpu = 0 
    noVOCPUs = []
    VOs_complete_list = []

    env = get_env_settings()
    log = env['LOG']
    print("\nLog Level = %s" %colourise("cyan", log))

    if log == "DEBUG":
       print("\n- Environment settings:")
       print(json.dumps(env, indent=4))

    # Fetching accounting records
    data = connect(env)

    accounting_period = env['DATE_FROM'][0:4] + "." + env['DATE_FROM'][-2:] + "-" + env['DATE_TO'][-2:]
    print(colourise("cyan", "\n[INFO]"), "    Reporting Period: %s" %accounting_period)

    try:
      for record in data:
        if "Percent" not in record['id'] and "Total" not in record['id']:
            if (record['Total']) > 0:
                VOs_complete_list.append({
                    "VO name": record['id'],
                    "CPU/h": format(record['Total'],"7,d")
                })

                total = total + 1
            else:
                noVOCPUs.append(record['id'])
                total_noVOCPUs = total_noVOCPUs + 1

        if "Total" in record['id']:
            if "cloud" in env['ACCOUNTING_SCOPE']: 
                print(colourise("green", "[Cloud]"), \
                        "   Total Cloud CPU/h = %s" %format(record['Total'],"7,d"))
                total_cloud_cpu = record['Total']
                    
                print(colourise("yellow", "[noVOCPUs]"), \
                      "VOs with *no* accounting records (%d)" %total_noVOCPUs)
                
                print(colourise("yellow", "[VOCPUs]"), \
                      "  VOs with *accounting* records (%d)" %total)
                
                if env['LOG'] == "DEBUG":
                   print(VOs_complete_list)

            else:  
                # Accounting records for the HTC resource centres
                print(colourise("green", "[HTC]"), \
                        "     Total HTC CPU/h = %s" %format(record['Total'],"7,d"))
                total_htc_cpu = record['Total']
                
                print(colourise("yellow", "[noVOCPUs]"), \
                     "VOs with *no* accounting records (%d)" %total_noVOCPUs)
                
                print(colourise("yellow", "[VOCPUs]"), \
                      "  VOs with *accounting* records (%d)" %total)
                
                if env['LOG'] == "DEBUG":
                   print(VOs_complete_list)

    except KeyError:
        pass

    # Update the accounting records in the Google Workspace based on the scope
    if env['ACCOUNTING_SCOPE'] == "cloud":
        update_GWorkSheet(env,
            accounting_period,
            total_cloud_cpu,
            noVOCPUs,
            total)

    else:
        update_GWorkSheet(env,
            accounting_period,
            total_htc_cpu,
            noVOCPUs,
            total)
        
 
if __name__ == "__main__":
        main()


