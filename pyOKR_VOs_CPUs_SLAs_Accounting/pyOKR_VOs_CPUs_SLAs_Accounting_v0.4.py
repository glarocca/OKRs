#!/usr/bin/env python3
#
#  Copyright 2025 EGI Foundation
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

import datetime
import json
import os
import requests
import warnings
warnings.filterwarnings("ignore")

from gspreadutils import init_GWorkSheet, init_SLAs_GWorkSheet
from utils import colourise, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.4"
__date__      = "$Date: 17/04/2025 10:50:22"
__copyright__ = "Copyright (c) 2025 EGI Foundation"
__license__   = "Apache Licence v2.0"


def get_accounting_data(env, vo_name):

    ''' Connecting to the EGI Accounting Portal '''

    data = ""
    _url = "%s/%s/%s/REGION/Year/%s/%s/custom-%s/%s/%s/%s/" %(env['ACCOUNTING_SERVER_URL'], 
            env['ACCOUNTING_SCOPE'],
            env['ACCOUNTING_METRIC'],
            env['DATE_FROM'], 
            env['DATE_TO'],
            vo_name,
            env['ACCOUNTING_LOCAL_JOB_SELECTOR'],
            env['ACCOUNTING_DATA_SELECTOR'],
            env['ACCOUNTING_DATA_SELECTOR'])

    headers = { "Accept": "Application/json" }

    try:
        curl = requests.get(url=_url, verify=True)
        data = curl.json()
    except ValueError:
        pass

    return _url, data



def get_GWorkSheetCellPosition(worksheet, accounting_period):
    ''' Get the cell coordinates where to add the new reporting period '''

    found = False
    pos = 2
    
    values_list = worksheet.col_values(1)

    if len(values_list) > 1:
       for header in values_list:
           if ("Period" not in header):
           
              if (header == accounting_period) or (header == ""):
                 found = True
                 break

              if header < accounting_period:
                 pos = pos + 1

    return(pos, found)



def get_vo_cell(worksheet, vo_name):
    ''' Insert the "vo_name" in the gspread if not present '''

    found = False
    vo_name_pos = 2
   
    # Get the full list of the headers in the gspread (row=1)
    values_list = worksheet.row_values(1)
    
    if len(values_list) > 1:
       for header in values_list:
           if ("Period" not in header):
              if (header == vo_name) or (header == ""):
                 found = True
                 break
              else:
                 vo_name_pos = vo_name_pos + 1
    
    if not found:
       print(colourise("green", "[INFO]"), \
             "Adding '%s' at column: %d" %(vo_name, vo_name_pos))
      
       worksheet.insert_cols(
               [[vo_name]],
               vo_name_pos,
               value_input_option='RAW',
               inherit_from_before=False)
    
    else:   
       print(colourise("green", "[INFO]"), \
             "The vo '%s' is *already* in the gspread at position: %s" %(vo_name, str(vo_name_pos)))

    return(vo_name_pos)  


def update_GWorkSheet(env, worksheet, accounting_period_pos, vo_name_pos, total_vo_cpu):
    ''' Update the accounting records in the Google Worksheet '''

    # Update the Google Worksheet cell (with the 'CPU/h' in the reporting period)
    worksheet.update_cell(accounting_period_pos, vo_name_pos, total_vo_cpu)

    if env['ACCOUNTING_SCOPE'] == "cloud":
       print(colourise("green", "[INFO]"), \
             "Updated the total Cloud CPU/h for the VO")
    else:
       print(colourise("green", "[INFO]"), \
             "Updated the total HTC CPU/h for the VO")


def getting_SLAs_metadata(env, SLAs_worksheet):
    ''' Retrieve the metadata of the active SLAs '''

    print(colourise("green", "\n[%s]" %env['LOG']), "Fetching the active *SLAs* in progress...")
    print("\tThis operation may take few minutes to complete. Please wait!")

    # Get the full list of the Customers 
    customers = SLAs_worksheet.get_all_values()

    VOs = []         

    values = SLAs_worksheet.get_all_values()
    for value in values:
        if ("VO name" not in value[10]): #and \
           #("vo.access.egi.eu" not in value[10]) and \
           #("training.egi.eu" not in value[10]) and \
           #("vo.notebooks.egi.eu" not in value[10]):
            if value[6] and "FINALIZED" in value[6]:
               if value[10] and value[12] and not value[16]:
                  VOs.append({
                     "Customer": value[0],
                     "Name": value[10],
                     "CPU/h": 0,
                     "Approval": value[9],
                     "SLA_start": value[7],
                     "SLA_end": value[8],
                     "Providers": "N/A",
                     "Active": "Y",
                     "Type": "egi"
                  })
               if value[10] and not value[12] and value[16]:
                  VOs.append({
                     "Customer": value[0],
                     "Name": value[10],
                     "CPU/h": 0,
                     "Approval": value[9],
                     "SLA_start": value[7],
                     "SLA_end": value[8],
                     "Providers": "N/A",
                     "Active": "Y",
                     "Type": "cloud"
                  })

               elif value[10] and value[12] and value[16]:
                  VOs.append({
                     "Customer": value[0],
                     "Name": value[10],
                     "CPU/h": 0,
                     "Approval": value[9],
                     "SLA_start": value[7],
                     "SLA_end": value[8],
                     "Providers": "N/A",
                     "Active": "Y",
                     "Type": "egi, cloud"
                  }) 

    #print(json.dumps(VOs, indent=4))

    # Saving active SLAs with metadata
    with open(env['ACTIVE_SLAs_FILE'], 'w', encoding='utf-8') as f:
         json.dump(VOs, f, ensure_ascii=False, indent=4)



def get_providers(env, customer, OLAs_worksheet):
    ''' Get the list of provider(s) supporting the given Customer '''

    providers_list = []
    total = 0

    # Get the list of provider(s) supporting the given Customer 
    providers = OLAs_worksheet.findall(customer)

    for provider in providers:
        provider_hostname = OLAs_worksheet.cell(provider.row, 2).value
        providers_list.append(provider_hostname)
        total = total + 1

    providers_string = ', '.join(providers_list)
    return(total, providers_string)



def main():

    dt = datetime.datetime.now()
    # Convert dt to string in dd-mm-yyyy HH:MM:SS
    now_timestamp = dt.strftime("%Y/%m")
    timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")

    env = get_env_settings()
    log = env['LOG']
    print("\nLog Level = %s" %colourise("cyan", log))

    print(colourise("green", "\n[%s]" %env['LOG']), "Environmental settings")
    print(json.dumps(env, indent=4))

    accounting_period = env['DATE_FROM'][0:4] + "." + env['DATE_FROM'][-2:] + "-" + env['DATE_TO'][-2:]

    # Initialise the GWorkSheet
    worksheet = init_GWorkSheet(env)
    SLAs_worksheet, OLAs_worksheet = init_SLAs_GWorkSheet(env)

    # Getting start_date, end_date of the active SLAs from the EGI_VOs_SLAs_OLAs_dashboard
    print(colourise("cyan", "\n[INFO]"), " Retrieve metadata of running SLAs in progress...")
    getting_SLAs_metadata(env, SLAs_worksheet)

    VOs_file = open(env['ACTIVE_SLAs_FILE'])
    VOs = json.load(VOs_file)

    # Formatting the header of the worksheet
    worksheet.format("A1:C1", {
      "backgroundColor": {
      "red": 55.0,
      "green": 15.0,
      "blue": 10.0
      },
      "horizontalAlignment": "LEFT",
      "textFormat": { "fontSize": 11, "bold": True }
    })

    # Formatting the cells of the worksheet
    worksheet.format("A2:C200", {
      "horizontalAlignment": "RIGHT",
      "textFormat": { "fontSize": 11 }
    })

    # Check the Headers of the gspread
    # 1.) Check whether the 'accounting_period' is already in the gspread
    accounting_period_pos, found_position = get_GWorkSheetCellPosition(worksheet, accounting_period)
    
    if (not found_position):
        print(colourise("cyan", "\n[INFO]"), \
             " Adding the reporting period at row:", accounting_period_pos)

        body = [accounting_period, total_cpu]
        worksheet.insert_row(body, index=accounting_period_pos, inherit_from_before=False)
    else:     
        print(colourise("green", "\n[INFO]"), \
              "The accounting_period *ALREADY FOUND* in the gspread at row: %s " \
              %accounting_period_pos)

    print(colourise("green", "\n[%s]" %env['LOG']), \
    "Downloading accounting records from the EGI Accouting Portal in progress...")
    print("\tThis operation may take few minutes to complete. Please wait!")

    total_cpu = 0
    
    for vo_details in VOs:
        if (env['ACCOUNTING_SCOPE'] in vo_details['Type']) and \
           (env['DATE_FROM'] >= vo_details['SLA_start']) and \
           (env['DATE_TO'] <= vo_details['SLA_end']) and \
            vo_details['Active'] == "Y":
            _url, data = get_accounting_data(env, vo_details['Name'])
            #total, providers = get_providers(env, vo_details['Customer'], OLAs_worksheet)

            try:
                if data:
                    print(colourise("cyan", "\n[INFO]"), \
                    " Fetching the accounting records for the VO [%s] in progress..." %vo_details['Name'].upper())
                  
                    if "DEBUG" in env['LOG']:
                       print(_url, data)
                       
                    for record in data:
                        if "Percent" not in record['id'] and "Total" not in record['id']:
                            print("- Resource Centre: %s; CPU/h: %s" %(record['id'], format(record['Total'],"7,d")))
                        if "Total" in record['id']:
                            if "cloud" in env['ACCOUNTING_SCOPE']:
                                print("- Total Cloud CPU/h = %s" %format(record['Total'],"7,d"))
                            else:
                                print("- Total HTC CPU/h = %s" %format(record['Total'],"7,d"))

                            #print("- Providers (%d): %s " %(total, providers))

                            vo_details['CPU/h'] = (int(vo_details['CPU/h']) + record['Total'])
                            total_cpu = total_cpu + record['Total']

                            # 2.) Check whether the 'vo_name' is already in the headers of the gspread
                            vo_name_pos = get_vo_cell(worksheet, vo_details['Name'])
                                   
                            #Update the CPU/h for the given VO in the gspread
                            update_GWorkSheet(env, 
                                    worksheet, 
                                    accounting_period_pos, 
                                    vo_name_pos,
                                    format(record['Total'],"7,d"))

            except (KeyError):
                pass

    total_cpu = format(total_cpu,"7,d")                   

    print(colourise("green", "\n[REPORT]"))
    if "cloud" in env['ACCOUNTING_SCOPE']:
       print("- Cloud CPU/h consumed by the EGI SLAs")
       print("- Reporting period = %s - %s" %(env['DATE_FROM'], env['DATE_TO']))
       print("- Total = %s Cloud CPU/h" %total_cpu.strip())
    else:
       print("- HTC CPU/h consumed by the EGI SLAs")
       print("- Reporting period = %s - %s" %(env['DATE_FROM'], env['DATE_TO']))
       print("- Total = %s HTC CPU/h" %total_cpu.strip())

    # Update the Total CPU/h consumed in the reporting period
    total_cell = worksheet.find("TOTAL")
    update_GWorkSheet(env,
            worksheet,
            accounting_period_pos,
            total_cell.col,
            total_cpu.strip())

    # Update the timestamp of the last update
    worksheet.insert_note("A1","Last update on: " + timestamp)  



if __name__ == "__main__":
        main()


