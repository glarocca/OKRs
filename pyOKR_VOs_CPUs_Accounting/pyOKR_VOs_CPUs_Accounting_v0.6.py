#!/usr/bin/env python3
#
#  Copyright 2024 EGI Foundation
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
import gspread
import json
import requests
import warnings
warnings.filterwarnings("ignore")

from gspreadutils import init_GWorkSheet
from utils import colourise, find_difference, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.6"
__date__      = "$Date: 02/06/2024 10:50:22"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def connect(env):
    ''' Connecting to the EGI Accounting Portal '''
    
    _url = "%s/%s/%s/VO/DATE/%s/%s/%s/%s/%s/%s/" %(env['ACCOUNTING_SERVER_URL'], 
            env['ACCOUNTING_SCOPE'],
            env['ACCOUNTING_METRIC'],
            env['DATE_FROM'], 
            env['DATE_TO'],
            env['ACCOUNTING_VO_GROUP_SELECTOR'],
            env['ACCOUNTING_LOCAL_JOB_SELECTOR'],
            env['ACCOUNTING_DATA_SELECTOR'],
            env['ACCOUNTING_DATA_SELECTOR'])

    headers = { "Accept": "Application/json" }
    
    if env['LOG'] == "DEBUG":
        print(colourise("cyan", "\n[INFO]"), \
              "- Fetching accounting records from: %s" %env['ACCOUNTING_SERVER_URL'])

    curl = requests.get(url=_url, headers=headers, verify=True)
    data = curl.json()

    return data


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
    

def update_GWorkSheet(env, worksheet, accounting_period, total_cpu, noVOsCPUs, totalVOCPUs, VOs_list):
    ''' Update the accounting records in the Google Worksheet '''

    # Formatting the header of the worksheet
    worksheet.format("A1:H1", {
      "backgroundColor": {
      "red": 55.0,
      "green": 15.0,
      "blue": 10.0
      },
      "horizontalAlignment": "LEFT",
      "textFormat": { "fontSize": 11, "bold": True }
    })

    # Formatting the cells of the worksheet
    worksheet.format("A2:H100", {
      "horizontalAlignment": "RIGHT",
      "textFormat": { "fontSize": 11 }
    })

    dt = datetime.datetime.now()
    # Convert dt to string in dd-mm-yyyy HH:MM:SS
    timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")

    # Convert list() to string
    VOs_string = ', '.join([str(elem['VO name']) for elem in VOs_list])
    NOVOs_string = ', '.join([str (item) for item in noVOsCPUs])

    flag = False # Accounting period not found in the GSpreadsheet
    worksheet_dicts = worksheet.get_all_records()
    
    for item in worksheet_dicts:
        if (item['Period'] == accounting_period):
           
           cell = worksheet.find(item['Period'])
           flag = True

           # Updating the cell of the Google Worksheet
           worksheet.update_cell(cell.row, cell.col + 1, total_cpu)
           
           # Total number of VOs with accounting
           worksheet.update_cell(cell.row, cell.col + 2, totalVOCPUs)
           
           # List of active VOs
           if VOs_string:
              worksheet.update_cell(cell.row, cell.col + 3, VOs_string)
           else:
              worksheet.update_cell(cell.row, cell.col + 3, '-')

           # Total number of VOs without accounting
           worksheet.update_cell(cell.row, cell.col + 4, len(noVOsCPUs))
        
           # VOs with *NO* accounting
           if len(noVOsCPUs):
              worksheet.update_cell(cell.row, cell.col + 5, NOVOs_string)
           else:   
              worksheet.update_cell(cell.row, cell.col + 5, '-')

           if (cell.row > 2):
               # Calculate VOs difference
               newVOs_str, leavingVOs_str = find_difference(
                       worksheet.cell(cell.row - 1, 4).value,
                       worksheet.cell(cell.row, 4).value)

               result = "APPEARED: " + newVOs_str + "\n" \
               "DISAPPEARED: " + leavingVOs_str

               worksheet.update_cell(cell.row, cell.col + 6, result)
           else:
               worksheet.update_cell(cell.row, cell.col + 6, '-')
           
           if env['ACCOUNTING_SCOPE'] == "cloud":
              print("Updated the Total Cloud CPU/h for the reporting period: %s" %accounting_period)
           else:   
              print("Updated the Total HTC CPU/h for the reporting period: %s" %accounting_period)

    if not flag:
           accounting_period_pos, found_position = get_GWorkSheetCellPosition(worksheet, accounting_period)
           print("Adding %s at row: %s" %(accounting_period, accounting_period_pos)) 
          
           if (accounting_period_pos > 2):
               newVOs_str, leavingVOs_str = find_difference(
                  worksheet.cell(accounting_period_pos, 4).value,
                  worksheet.cell(accounting_period_pos - 1, 4).value)

               result = "APPEARED: " + newVOs_str + "\n" \
               "DISAPPEARED: " + leavingVOs_str

               body = [accounting_period, 
                       total_cpu, 
                       totalVOCPUs, 
                       VOs_string,
                       len(noVOsCPUs),
                       NOVOs_string,
                       str(result)]
           else:
               body = [accounting_period,
                       total_cpu,
                       totalVOCPUs,
                       VOs_string,
                       len(noVOsCPUs),
                       NOVOs_string,
                       '-']

           worksheet.insert_row(body, index=accounting_period_pos, inherit_from_before=True)

    # Update the timestamp of the last update
    worksheet.insert_note("A1","Last update on: " + timestamp)


def main():

    # Initialise environment variables
    total = total_noVOsCPUs = total_cloud_cpu = total_htc_cpu = 0 
    noVOsCPUs = []
    VOs_complete_list = []

    env = get_env_settings()
    log = env['LOG']
    print("\nLog Level = %s" %colourise("cyan", log))

    # Initialise the GWorkSheet
    worksheet = init_GWorkSheet(env)

    if log == "DEBUG":
       print("\n- Environment settings:")
       print(json.dumps(env, indent=4))

    # Fetching accounting records
    data = connect(env)

    accounting_period = env['DATE_FROM'][0:4] + "." + env['DATE_FROM'][-2:] + "-" + env['DATE_TO'][-2:]
    print(colourise("cyan", "\n[INFO]"), "     Reporting Period: %s" %accounting_period)

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
                noVOsCPUs.append(record['id'])
                total_noVOsCPUs = total_noVOsCPUs + 1

        if "Total" in record['id']:
            if "cloud" in env['ACCOUNTING_SCOPE']: 
                print(colourise("green", "[Cloud]"), \
                        "    Total Cloud CPU/h = %s" %format(record['Total'],"7,d"))
                total_cloud_cpu = record['Total']
                    
                print(colourise("yellow", "[noVOsCPUs]"), \
                      "VOs with *no* accounting records (%d)" %total_noVOsCPUs)
                
                if env['LOG'] == "DEBUG":
                    if len(noVOsCPUs)>0:
                        print(noVOsCPUs)
                
                print(colourise("yellow", "[VOCPUs]"), \
                      "   VOs with *accounting* records (%d)" %total)
                
                if env['LOG'] == "DEBUG":
                   VOs_string = ', '.join([str(elem['VO name']) for elem in VOs_complete_list])
                   print(VOs_string)

            else:  
                # Accounting records for the HTC resource centres
                print(colourise("green", "[HTC]"), \
                        "      Total HTC CPU/h = %s" %format(record['Total'],"7,d"))
                total_htc_cpu = record['Total']
                
                print(colourise("yellow", "[noVOsCPUs]"), \
                     "VOs with *no* accounting records (%d)" %total_noVOsCPUs)
                
                if env['LOG'] == "DEBUG":
                    if len(noVOsCPUs)>0:
                        print(noVOsCPUs)
               
                print(colourise("yellow", "[VOCPUs]"), \
                      "   VOs with *accounting* records (%d)" %total)

                if env['LOG'] == "DEBUG":
                   VOs_string = ', '.join([str(elem['VO name']) for elem in VOs_complete_list])
                   print(VOs_string)
                
    except KeyError:
        pass

    # Update the accounting records in the Google Workspace based on the scope
    if env['ACCOUNTING_SCOPE'] == "cloud":
        update_GWorkSheet(env,
            worksheet,    
            accounting_period,
            total_cloud_cpu,
            noVOsCPUs,
            total,
            VOs_complete_list)
    else:
        update_GWorkSheet(env,
            worksheet,    
            accounting_period,
            total_htc_cpu,
            noVOsCPUs,
            total,
            VOs_complete_list)
        
 
if __name__ == "__main__":
        main()


