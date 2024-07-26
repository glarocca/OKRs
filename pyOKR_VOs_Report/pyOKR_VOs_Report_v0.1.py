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

import datetime
import gspread
import json
import requests
import warnings

warnings.filterwarnings("ignore")

from gspreadutils import init_GWorkSheet
from operationsutils import get_VOs_report
from utils import colourise, find_difference, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.1"
__date__      = "$Date: 04/11/2023 10:50:22"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__   = "Apache Licence v2.0"


def get_GWorkSheetCellPosition(worksheet, reporting_period):
    ''' Get the cell coordinates where to add the new reporting period '''

    found = False
    pos = 2

    values_list = worksheet.col_values(1)

    if len(values_list) > 1:
       for header in values_list:
           if ("Period" not in header):

              if (header == reporting_period) or (header == ""):
                 found = True
                 break

              if header < reporting_period:
                 pos = pos + 1

    return(pos, found)
    

def update_GWorkSheet(env, worksheet, reporting_period, VOs_report):
    ''' Update the reporting records in the Google Worksheet '''

    # Formatting the header of the worksheet
    worksheet.format("A1:E1", {
      "backgroundColor": {
      "red": 55.0,
      "green": 15.0,
      "blue": 10.0
      },
      "horizontalAlignment": "LEFT",
      "textFormat": { "fontSize": 11, "bold": True }
    })

    # Formatting the cells of the worksheet
    worksheet.format("A2:E100", {
      "horizontalAlignment": "RIGHT",
      "textFormat": { "fontSize": 11 }
    })

    dt = datetime.datetime.now()
    # Convert dt to string in dd-mm-yyyy HH:MM:SS
    timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")

    total = 0
    total_deleted = 0
    total_production = 0
    for VO in VOs_report:
        total = total + int(VO['count'])
        for value in VO.items():
            if "Deleted" in value:
                total_deleted = int(VO['count'])
                #print("Deleted VOs: %d" %total_deleted)

            if "Production" in value:
                total_production = int(VO['count'])
                #print("Production VOs: %d" %total_production)


    # Convert list() to string
    VOs_string = ', '.join([str(elem['vos']) for elem in VOs_report])

    flag = False # Reporting period not found in the GSpreadsheet
    worksheet_dicts = worksheet.get_all_records()
    for item in worksheet_dicts:
        if (item['Period'] == reporting_period):
           
           cell = worksheet.find(item['Period'])
           flag = True

           # Updating the total number of VOs in the reporting period
           worksheet.update_cell(cell.row, cell.col + 1, total)
           
           # Updating the total number of VOs with Status = 'Deleted' in the reporting period
           worksheet.update_cell(cell.row, cell.col + 2, total_deleted)
           # Updating the total number of VOs with Status = 'Production' in the reporting period
           worksheet.update_cell(cell.row, cell.col + 3, total_production)
           
           # Update the VOs report
           if VOs_string:
              worksheet.update_cell(cell.row, cell.col + 4, VOs_string)
           else:
              worksheet.update_cell(cell.row, cell.col + 4, '-')

           print(colourise("cyan", "[INFO]"), \
           " Updated the VOs reports for the reporting period: %s" %reporting_period)
           
    if not flag:
           reporting_period_pos, found_position = get_GWorkSheetCellPosition(worksheet, reporting_period)
           print(colourise("cyan", "\n[INFO]"), \
           " Adding reporting period: %s at row: %s" %(reporting_period, reporting_period_pos))
          
           body = [reporting_period, 
                   total,
                   total_deleted,
                   total_production,
                   VOs_string]

           index = get_GWorkSheetCellPosition(worksheet, reporting_period)
           worksheet.insert_row(body, index=reporting_period_pos, inherit_from_before=True)
           
           print(colourise("cyan", "[INFO]"), \
           " Updated the VOs reports for the reporting period: %s" %reporting_period)

    # Update the timestamp of the last update
    worksheet.insert_note("A1","Last update on: " + timestamp)


def main():

    env = get_env_settings()
    log = env['LOG']
    print("\nLog Level = %s" %colourise("cyan", log))

    if log == "DEBUG":
       print("\n- Environment settings:")
       print(json.dumps(env, indent=4))

    reporting_period = env['DATE_FROM'][0:4] + "." + env['DATE_FROM'][-2:] + "-" + env['DATE_TO'][-2:]
    print(colourise("cyan", "\n[INFO]"), " Reporting Period: %s" %reporting_period)

    # Initialise the GWorkSheet
    worksheet = init_GWorkSheet(env)

    # Get the list of VOs created and deleted in the reporting period
    VOs_report = get_VOs_report(env)
    if log == "DEBUG":
       print(colourise("green", "\n[LOG]"), \
       "  List of VOs creation and deletion during the reporting period \n%s" %json.dumps(VOs_report, indent=4))

    update_GWorkSheet(env, worksheet, reporting_period, VOs_report)
        
 
if __name__ == "__main__":
        main()


