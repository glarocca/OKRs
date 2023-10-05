#!/usr/bin/env python3
#
#  Copyright 2023 EGI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import gspread
import json
import re
import requests
import time

from datetime import datetime
from utils import colourise, highlight, get_env_settings
from jirautils import getCustomersComplains, getServiceOrders

__author__ = "Giuseppe LA ROCCA"
__email__ = "giuseppe.larocca@egi.eu"
__version__ = "$Revision: 0.4"
__date__ = "$Date: 04/10/2023 06:55:17"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__ = "Apache Licence v2.0"


def init_GWorkSheet(env):
    """Initialise the GWorkSheet settings and return the worksheet"""

    # Get the service account
    account = gspread.service_account(env["SERVICE_ACCOUNT_FILE"])
    # Open the GoogleSheet
    sheet = account.open(env["GOOGLE_SHEET_NAME"])
    # Open the Worksheet
    worksheet = sheet.worksheet(env["GOOGLE_SERVICE_ORDERS_WORKSHEET"])

    return worksheet


def update_GWorkSheet_Headers(env, worksheet, reporting_period):
    """Insert new header in the worksheet (if not present)"""

    y_pos = 2
    flag = True

    worksheet_dicts = worksheet.get_all_records()
    for header in worksheet_dicts[0]:
        if "Services" not in header:
            if header == reporting_period:
                y_pos = -1
                break
            if header < reporting_period:
                y_pos = y_pos + 1
            else:
                break

    if y_pos >= 2 or y_pos > len(worksheet_dicts[0]):
        flag = False

    if not flag:
        print("Adding '%s' at column: %s" % (reporting_period, y_pos))
        worksheet.insert_cols(
            [[reporting_period]],
            y_pos,
            value_input_option="RAW",
            inherit_from_before=True,
        )
    else:
        print("The header '%s' is *already* in the Worksheet" % reporting_period)


def get_GWorkSheet_HeaderPosition(env, worksheet, reporting_period):
    """Get the columnID of the specific header (based on the reporting_period)"""

    headers_list = worksheet.row_values(1)
    col = 2

    for header in headers_list:
        if "Services" not in header:
            if header != reporting_period:
                col = col + 1
            else:
                break

    return col


def get_GWorkSheet_SOPosition(worksheet, service):
    """Get the rowID where to add the new service in the worksheet"""

    flag = False
    row = 3

    worksheet_dicts = worksheet.get_all_records()
    for worksheet_dict in worksheet_dicts:
        if "TOTAL" not in worksheet_dict["Services"]:
            if worksheet_dict["Services"] <= service:
                row = row + 1
            else:
                flag = True
                break

    return row


def update_GWorkSheet_SOs(env, worksheet, EGI_SOs, reporting_period):
    """Update the Service Orders (SOs) in the Google Workseet"""

    # Formatting the header of the worksheet
    worksheet.format(
        "A1:P1",
        {
            "backgroundColor": {"red": 55.0, "green": 15.0, "blue": 10.0},
            "horizontalAlignment": "LEFT",
            "textFormat": {"fontSize": 11, "bold": True},
        },
    )

    # Formatting the cells of the worksheet
    worksheet.format(
        "A2:P30", {"horizontalAlignment": "RIGHT", "textFormat": {"fontSize": 10}}
    )

    # 1.) Update of the SOs for the EGI services already existing in the worksheet
    print(
        colourise("cyan", "\n[INFO]"),
        " Updating the Service Orders of the EGI services *already existing* in the worksheet in progress..",
    )
    print("\tThis operation may take few minutes. Please wait!\n")

    # Identify the proper column IDs
    Period_cell = worksheet.find(reporting_period)

    worksheet_dicts = worksheet.get_all_records()
    for worksheet_dict in worksheet_dicts:
        try:
            if worksheet_dict["Services"] == "EGI Cloud Compute":
                service_orders = ", ".join(EGI_SOs["EGI Cloud Compute"])
                Cloud_Compute_cell = worksheet.find("EGI Cloud Compute")
                worksheet.update_cell(
                    Cloud_Compute_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Cloud Compute"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(Cloud_Compute_cell.row, Period_cell.col),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Cloud Compute"
                    % len(EGI_SOs["EGI Cloud Compute"])
                )
                EGI_SOs.pop("EGI Cloud Compute")

            if worksheet_dict["Services"] == "EGI Cloud Container Compute":
                service_orders = ", ".join(EGI_SOs["EGI Cloud Container Compute"])
                Cloud_Container_Compute_cell = worksheet.find(
                    "EGI Cloud Container Compute"
                )
                worksheet.update_cell(
                    Cloud_Container_Compute_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Cloud Container Compute"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        Cloud_Container_Compute_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Cloud Container Compute"
                    % len(EGI_SOs["EGI Cloud Container Compute"])
                )
                EGI_SOs.pop("EGI Cloud Container Compute")

            if worksheet_dict["Services"] == "EGI High-Throughput Compute":
                service_orders = ", ".join(EGI_SOs["EGI High-Throughput Compute"])
                High_Throughput_Compute_cell = worksheet.find(
                    "EGI High-Throughput Compute"
                )
                worksheet.update_cell(
                    High_Throughput_Compute_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI High-Throughput Compute"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        High_Throughput_Compute_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI High-Throughput Compute"
                    % len(EGI_SOs["High-Throughput Compute"])
                )
                EGI_SOs.pop("EGI High-Throughput Compute")

            if worksheet_dict["Services"] == "EGI Software Distribution":
                service_orders = ", ".join(EGI_SOs["EGI Software Distribution"])
                Software_Distribution_cell = worksheet.find("EGI Software Distribution")
                worksheet.update_cell(
                    Software_Distribution_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Software Distribution"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        Software_Distribution_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Software Distribution"
                    % len(EGI_SOs["EGI Software Distribution"])
                )
                EGI_SOs.pop("EGI Software Distribution")

            if worksheet_dict["Services"] == "EGI Workload Manager":
                service_orders = ", ".join(EGI_SOs["EGI Workload Manager"])
                Workload_Manager_cell = worksheet.find("EGI Workload Manager")
                worksheet.update_cell(
                    Workload_Manager_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Workload Manager"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        Workload_Manager_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Workload Manager"
                    % len(EGI_SOs["EGI Workload Manager"])
                )
                EGI_SOs.pop("EGI Workload Manager")

            if worksheet_dict["Services"] == "EGI Infrastructure Manager":
                service_orders = ", ".join(EGI_SOs["EGI Infrastructure Manager"])
                Infrastructure_Manager_cell = worksheet.find(
                    "EGI Infrastructure Manager"
                )
                worksheet.update_cell(
                    Infrastructure_Manager_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Infrastructure Manager"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        Infrastructure_Manager_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Infrastructure Manager"
                    % len(EGI_SOs["EGI Infrastructure Manager"])
                )
                EGI_SOs.pop("EGI Infrastructure Manager")

            if worksheet_dict["Services"] == "EGI Online Storage":
                service_orders = ", ".join(EGI_SOs["EGI Online Storage"])
                Online_Storage_cell = worksheet.find("EGI Online Storage")
                worksheet.update_cell(
                    Online_Storage_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Online Storage"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        Online_Storage_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Online Storage"
                    % len(EGI_SOs["EGI Online Storage"])
                )
                EGI_SOs.pop("EGI Online Storage")

            if worksheet_dict["Services"] == "EGI Data Transfer":
                service_orders = ", ".join(EGI_SOs["EGI Data Transfer"])
                Data_Transfer_cell = worksheet.find("EGI Data Transfer")
                worksheet.update_cell(
                    Data_Transfer_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Data Transfer"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(Data_Transfer_cell.row, Period_cell.col),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Data Transfer"
                    % len(EGI_SOs["EGI Data Transfer"])
                )
                EGI_SOs.pop("EGI Data Transfer")

            if worksheet_dict["Services"] == "EGI DataHub":
                service_orders = ", ".join(EGI_SOs["EGI DataHub"])
                DataHub_cell = worksheet.find("EGI DataHub")
                worksheet.update_cell(
                    DataHub_cell.row, Period_cell.col, len(EGI_SOs["EGI DataHub"])
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(DataHub_cell.row, Period_cell.col),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI DataHub"
                    % len(EGI_SOs["EGI DataHub"])
                )
                EGI_SOs.pop("EGI DataHub")

            if worksheet_dict["Services"] == "EGI Check-In":
                service_orders = ", ".join(EGI_SOs["EGI Check-In"])
                Check_In_cell = worksheet.find("EGI Check-In")
                worksheet.update_cell(
                    Check_In_cell.row, Period_cell.col, len(EGI_SOs["EGI Check-In"])
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(Check_In_cell.row, Period_cell.col),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Check-In"
                    % len(EGI_SOs["EGI Check-In"])
                )
                EGI_SOs.pop("EGI Check-In")

            if worksheet_dict["Services"] == "EGI Notebooks":
                service_orders = ", ".join(EGI_SOs["EGI Notebooks"])
                Notebooks_cell = worksheet.find("EGI Notebooks")
                worksheet.update_cell(
                    Notebooks_cell.row, Period_cell.col, len(EGI_SOs["EGI Notebooks"])
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(Notebooks_cell.row, Period_cell.col),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Notebooks"
                    % len(EGI_SOs["EGI Notebooks"])
                )
                EGI_SOs.pop("EGI Notebooks")

            if worksheet_dict["Services"] == "EGI Replay":
                service_orders = ", ".join(EGI_SOs["EGI Replay"])
                Replay_cell = worksheet.find("EGI Replay")
                worksheet.update_cell(
                    Replay_cell.row, Period_cell.col, len(EGI_SOs["EGI Replay"])
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(Replay_cell.row, Period_cell.col),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Replay"
                    % len(EGI_SOs["EGI Replay"])
                )
                EGI_SOs.pop("EGI Replay")

            if worksheet_dict["Services"] == "EGI FitSM Training":
                service_orders = ", ".join(EGI_SOs["EGI FitSM Training"])
                FitSM_Training_cell = worksheet.find("EGI FitSM Training")
                worksheet.update_cell(
                    FitSM_Training_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI FitSM Training"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        FitSM_Training_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI FitSM Training"
                    % len(EGI_SOs["EGI FitSM Training"])
                )
                EGI_SOs.pop("EGI FitSM Training")

            if worksheet_dict["Services"] == "EGI ISO 27001 Training":
                service_orders = ", ".join(EGI_SOs["EGI ISO 27001 Training"])
                ISO_27001_Training_cell = worksheet.find("EGI ISO 27001 Training")
                worksheet.update_cell(
                    ISO_27001_Training_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI ISO 27001 Training"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        ISO_27001_Training_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI ISO 27001 Training"
                    % len(EGI_SOs["EGI ISO 27001 Training"])
                )
                EGI_SOs.pop("EGI ISO 27001 Training")

            if worksheet_dict["Services"] == "EGI Training Infrastructure":
                service_orders = ", ".join(EGI_SOs["EGI Training Infrastructure"])
                Training_Infrastructure_cell = worksheet.find(
                    "EGI Training Infrastructure"
                )
                worksheet.update_cell(
                    Training_Infrastructure_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Training Infrastructure"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(
                        Training_Infrastructure_cell.row, Period_cell.col
                    ),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Training Infrastructure"
                    % len(EGI_SOs["EGI Training Infrastructure"])
                )
                EGI_SOs.pop("EGI Training Infrastructure")

            if worksheet_dict["Services"] == "EGI Dynamic DNS":
                service_orders = ", ".join(EGI_SOs["EGI Dynamic DNS"])
                Dynamic_DNS_cell = worksheet.find("EGI Dynamic DNS")
                worksheet.update_cell(
                    Dynamic_DNS_cell.row,
                    Period_cell.col,
                    len(EGI_SOs["EGI Dynamic DNS"]),
                )

                # Converting row and column cell address to A1 notation
                worksheet.insert_note(
                    gspread.utils.rowcol_to_a1(Dynamic_DNS_cell.row, Period_cell.col),
                    service_orders,
                )

                print(
                    "Updated the #SOs [%d] for the service: EGI Dynamic DNS"
                    % len(EGI_SOs["Dynamic DNS"])
                )
                EGI_SOs.pop("EGI Dynamic DNS")

        except:
            print(
                colourise("red", "[WARNING]"),
                "Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'",
            )
            time.sleep(60)
            EGI_SOs.pop(worksheet_dict["Services"])

    print(
        colourise("cyan", "[INFO]"), " Service Orders updated in the Google worksheet!"
    )

    # 2.) Insert new EGI services with its metrics in the worksheet
    if len(EGI_SOs) > 0:
        print(
            colourise("cyan", "\n[INFO]"),
            "\tAdding *new EGI services* (and related Service Orders) in the Google worksheet in progress..",
        )
        print("\tThis operation may take few minutes. Please wait!")

    # Identify the proper column ID for the SO
    col_index = get_GWorkSheet_HeaderPosition(env, worksheet, reporting_period)

    for service, SOs in EGI_SOs.items():
        try:
            service_orders = ", ".join(EGI_SOs[service])
            service_cell = worksheet.find(service)
            row_index = get_GWorkSheet_SOPosition(worksheet, service)
            print(
                "Insert the EGI Service [%s] at: (%d, %d)"
                % (service, row_index, col_index)
            )

            # Insert a new row in the worksheet
            body = ["", ""]
            worksheet.insert_row(body, index=row_index)

            # Update the cells with the *new* service
            worksheet.update_cell(row_index, 1, service)

            # Update the Google Worksheet cell (with the 'Num. of SOs' in the reporting period)
            worksheet.update_cell(row_index, col_index, len(EGI_SOs[service]))

            # Adding details of the SOs as a note in the cell
            worksheet.insert_note(
                gspread.utils.rowcol_to_a1(row_index, col_index), service_orders
            )

            print("Added SOs for the service: %s" % service)

        except:
            print(
                colourise("red", "[WARNING]"),
                "Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'",
            )
            time.sleep(60)

    if len(EGI_SOs) > 0:
        print(
            colourise("cyan", "[INFO]"),
            " *New* EGI services [%d] added in the Google worksheet!" % len(EGI_SOs),
        )


def main():
    # Initialise env. variables
    service_orders = []
    service_orders_list = []

    EGI_SOs = {
        "EGI Cloud Compute": "0",
        "EGI Cloud Container Compute": "0",
        "EGI High-Throughput Compute": "0",
        "EGI Software Distribution": "0",
        "EGI Workload Manager": "0",
        "EGI Infrastructure Manager": "0",
        "EGI Online Storage": "0",
        "EGI Data Transfer": "0",
        "EGI DataHub": "0",
        "EGI Check-In": "0",
        "EGI Notebooks": "0",
        "EGI Replay": "0",
        "EGI FitSM Training": "0",
        "EGI ISO 27001 Training": "0",
        "EGI Training Infrastructure": "0",
        "EGI Dynamic DNS": "0",
    }

    EGI_Cloud_Compute = 0
    EGI_Cloud_Container_Compute = 0
    EGI_High_Throughput_Compute = 0
    EGI_Software_Distribution = 0
    EGI_Workload_Manager = 0
    EGI_Infrastructure_Manager = 0
    EGI_Online_Storage = 0
    EGI_Data_Transfer = 0
    EGI_DataHub = 0
    EGI_Check_In = 0
    EGI_Notebooks = 0
    EGI_Replay = 0
    EGI_FitSM_Training = 0
    EGI_ISO_27001_Training = 0
    EGI_Training_Infrastructure = 0
    EGI_Dynamic_DNS_service = 0

    # Initialise the environment settings
    env = get_env_settings()
    print("\nLog Level = %s" % colourise("cyan", env["LOG"]))
    print("\nGenerating reporting in progress...")
    print("This operation may take a few minutes to complete. Please wait!")

    reporting_period = (
        env["DATE_FROM"][0:4] + "." + env["DATE_FROM"][-2:] + "-" + env["DATE_TO"][-2:]
    )

    print(colourise("cyan", "\n[INFO]"), "Reporting Period = %s" % reporting_period)

    # Initialise the GWorkSheet
    worksheet = init_GWorkSheet(env)

    # Update the headers of the GWorkSheet (if necessary)
    update_GWorkSheet_Headers(env, worksheet, reporting_period)

    # Retrieve the number of total issues of a given projectKey
    service_orders = getServiceOrders(env, service_orders)
    # print(json.dumps(orders, indent=4, sort_keys=False))

    start = (env["DATE_FROM"].replace("/", "-")) + "-01"
    end = (env["DATE_TO"].replace("/", "-")) + "-01"

    for service_order in service_orders:
        service_order_dict = []
        _tmp = ""

        if (
            env["SERVICE_ORDERS_ISSUETYPE"]
            in service_order["fields"]["issuetype"]["name"]
        ):
            details = service_order["fields"]["customfield_10711"]
            for match in re.finditer('"service"', details.strip(), re.IGNORECASE):
                # Start and final index of the match
                start = match.start()
                end = match.end()
                # print(details)
                _tmp = details[end + 1 : -1].split(",", 1)[0]

            if service_order["fields"]["assignee"]:
                assignee = service_order["fields"]["assignee"]

                service_order_dict = {
                    "SO": service_order["key"],
                    "URL": env["JIRA_SERVER_URL"] + "browse/" + service_order["key"],
                    # "EPIC": env['JIRA_SERVER_URL'] + "browse/" + service_order['fields']['customfield_10100'],
                    "Issue Type": service_order["fields"]["issuetype"]["name"],
                    "Status": service_order["fields"]["status"]["name"].upper(),
                    "Created": service_order["fields"]["created"],
                    "Assignee": assignee["displayName"],
                    # "Service": service_order['fields']['customfield_10711']
                    # Remove the \" at the beginning and the end of the string
                    "Service": _tmp[1 : len(_tmp) - 1],
                }

            else:
                service_order_dict = {
                    "SO": service_order["key"],
                    "URL": env["JIRA_SERVER_URL"] + "browse/" + service_order["key"],
                    # "EPIC": env['JIRA_SERVER_URL'] + "browse/" + service_order['fields']['customfield_10100'],
                    "Issue Type": service_order["fields"]["issuetype"]["name"],
                    "Status": service_order["fields"]["status"]["name"].upper(),
                    "Created": service_order["fields"]["created"],
                    # "Service": service_order['fields']['customfield_10711']
                    # Remove the \" at the beginning and the end of the string
                    "Service": _tmp[1 : len(_tmp) - 1],
                }

            if env["LOG"] == "DEBUG":
                print(
                    colourise("green", "\n[LOG]"),
                    "Service Order (SO) received via the EOSC MarketPlace [%d]"
                    % len(service_orders_list),
                )
                print(service_order_dict)
                # print(json.dumps(service_orders_dict, indent=4, sort_keys=False))

            service_orders_list.append(service_order_dict)

    EGI_Cloud_Compute_SOs = []
    EGI_Cloud_Container_Compute_SOs = []
    EGI_High_Throughput_Compute_SOs = []
    EGI_Software_Distribution_SOs = []
    EGI_Workload_Manager_SOs = []
    EGI_Infrastructure_Manager_SOs = []
    EGI_Online_Storage_SOs = []
    EGI_Data_Transfer_SOs = []
    EGI_DataHub_SOs = []
    EGI_Check_In_SOs = []
    EGI_Notebooks_SOs = []
    EGI_Replay_SOs = []
    EGI_FitSM_Training_SOs = []
    EGI_ISO_27001_Training_SOs = []
    EGI_Training_Infrastructure_SOs = []
    EGI_Dynamic_DNS_SOs = []

    for service_order in service_orders_list:
        if service_order["Service"].lower() in "EGI Cloud Compute".lower():
            EGI_Cloud_Compute_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI Cloud Container Compute".lower():
            EGI_Cloud_Container_Compute_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI High-Throughput Compute".lower():
            EGI_High_Throughput_Compute_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "Sofware Distribution".lower():
            EGI_Software_Distribution_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "Workload Manager".lower():
            EGI_Workload_Manager_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "Infrastructure Manager".lower():
            EGI_Infrastructure_Manager_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI Online Storage".lower():
            EGI_Online_Storage_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI Data Transfer".lower():
            EGI_Data_Transfer_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI DataHub".lower():
            EGI_DataHub_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI Check-In".lower():
            EGI_Check_In_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI Notebooks".lower():
            EGI_Notebooks_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI Replay".lower():
            EGI_Replay_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI FitSM Training".lower():
            EGI_FitSM_Training_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI ISO 27001 Training".lower():
            EGI_ISO_27001_Training_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "EGI Training Infrastructure".lower():
            EGI_Training_Infrastructure_SOs.append(service_order["SO"])
        elif service_order["Service"].lower() in "Dynamic DNS".lower():
            EGI_Dynamic_DNS_SOs.append(service_order["SO"])

    EGI_SOs = {
        "EGI Cloud Compute": EGI_Cloud_Compute_SOs,
        "EGI Cloud Container Compute": EGI_Cloud_Container_Compute_SOs,
        "EGI High-Throughput Compute": EGI_High_Throughput_Compute_SOs,
        "EGI Software Distribution": EGI_Software_Distribution_SOs,
        "EGI Workload Manager": EGI_Workload_Manager_SOs,
        "EGI Infrastructure Manager": EGI_Infrastructure_Manager_SOs,
        "EGI Online Storage": EGI_Online_Storage_SOs,
        "EGI Data Transfer": EGI_Data_Transfer_SOs,
        "EGI DataHub": EGI_DataHub_SOs,
        "EGI Check-In": EGI_Check_In_SOs,
        "EGI Notebooks": EGI_Notebooks_SOs,
        "EGI Replay": EGI_Replay_SOs,
        "EGI FitSM Training": EGI_FitSM_Training_SOs,
        "EGI ISO 27001 Training": EGI_ISO_27001_Training_SOs,
        "EGI Training Infrastructure": EGI_Training_Infrastructure_SOs,
        "EGI Dynamic DNS": EGI_Dynamic_DNS_SOs,
    }

    if env["LOG"] == "DEBUG":
        print(
            colourise("cyan", "\n[INFO]"),
            " EOSC service orders received for the EGI services in the reporting period %s"
            % reporting_period,
        )
        print(json.dumps(EGI_SOs, indent=4, sort_keys=False))

    # Update the GWorkSheet
    update_GWorkSheet_SOs(env, worksheet, EGI_SOs, reporting_period)


if __name__ == "__main__":
    main()
