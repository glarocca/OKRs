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
import time
import warnings

warnings.filterwarnings("ignore")
from operationsutils import get_VO_users, get_VO_stats, get_VOs_stats, get_VO_metadata
from utils import colourise, highlight, get_env_settings

__author__ = "Giuseppe LA ROCCA"
__email__ = "giuseppe.larocca@egi.eu"
__version__ = "$Revision: 0.5"
__date__ = "$Date: 14/11/2023 18:23:17"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__ = "Apache Licence v2.0"


def init_GWorkSheet(env):
    """Initialise the GWorkSheet settings and return the worksheet"""

    # Get the service account
    account = gspread.service_account(env["SERVICE_ACCOUNT_FILE"])
    # Open the GoogleSheet
    sheet = account.open(env["GOOGLE_SHEET_NAME"])
    # Open the Worksheet
    worksheet = sheet.worksheet(env["GOOGLE_VOS_WORKSHEET"])

    return worksheet


def get_GWorkSheet_HeaderPosition(env, worksheet, accounting_period):
    """Get the columnID of the specific header (based on the accounting_period)"""

    headers_list = worksheet.row_values(1)
    col = 2

    for header in headers_list:
        if "VO" not in header:
            if header != accounting_period:
                col = col + 1
            else:
                break

    return col


def get_GWorkSheet_VOPosition(worksheet, VO_name):
    """Get the rowID where to add the new VO in the worksheet"""

    flag = False
    row = 3

    worksheet_dicts = worksheet.get_all_records()
    for worksheet_dict in worksheet_dicts:
        if "TOTAL" not in worksheet_dict["VO"]:
            if worksheet_dict["VO"] <= VO_name:
                row = row + 1
            else:
                flag = True
                break

    return row


def update_GWorkSheet_Headers(env, worksheet, accounting_period):
    """Insert new header in the worksheet (if not present)"""

    y_pos = 2
    flag = True

    worksheet_dicts = worksheet.get_all_records()
    for header in worksheet_dicts[0]:
        if "VO" not in header:
            if header == accounting_period:
                y_pos = -1
                break
            if header < accounting_period:
                y_pos = y_pos + 1
            else:
                break

    if y_pos >= 2 or y_pos > len(worksheet_dicts[0]):
        flag = False

    if not flag:
        print("Adding '%s' at column: %s" % (accounting_period, y_pos))
        worksheet.insert_cols(
            [[accounting_period]],
            y_pos,
            value_input_option="RAW",
            inherit_from_before=True,
        )
    else:
        print("\tThe header '%s' is *already* in the Worksheet" % accounting_period)


def update_GWorkSheet_VOs(env, worksheet, VOs_list, accounting_period):
    """Update the accounting records for the VOs in the Google Worksheet"""

    # Formatting the header of the worksheet
    worksheet.format(
        "A1:B1",
        {
            "backgroundColor": {"red": 55.0, "green": 15.0, "blue": 10.0},
            "horizontalAlignment": "LEFT",
            "textFormat": {"fontSize": 11, "bold": True},
        },
    )

    # Formatting the cells of the worksheet
    worksheet.format(
        "A2:Z30", {"horizontalAlignment": "RIGHT", "textFormat": {"fontSize": 10}}
    )

    # 1.) Update VO metrics already existing in the worksheet
    print(
        colourise("cyan", "\n[INFO]"),
        "\tUpdating statistics of the VOs *already existing* in the Google worksheet in progress..",
    )
    print("\tThis operation may take few minutes. Please wait!")

    worksheet_dicts = worksheet.get_all_records()
    # Identify the proper column ID
    Period_cell = worksheet.find(accounting_period)
    Registered_Users_cell = worksheet.find("Registered Users")
    Total_Users_cell = worksheet.find("Total Users")

    for worksheet_dict in worksheet_dicts:
        index = 0
        while index < len(VOs_list):
            try:
                if worksheet_dict["VO"] == VOs_list[index]["name"]:
                    # Find the proper cell where update the VO metadata
                    VO_cell = worksheet.find(worksheet_dict["VO"])

                    # Update the Google Worksheet cell (with the 'Num. of users' in the reporting period)
                    worksheet.update_cell(
                        VO_cell.row, Period_cell.col, VOs_list[index]["users"]
                    )

                    # Update the Google Worksheet cell (with the 'Registered' users)
                    worksheet.update_cell(
                        VO_cell.row,
                        Registered_Users_cell.col,
                        VOs_list[index]["active_members"],
                    )

                    # Update the Google Worksheet cell (with the 'Total' users)
                    worksheet.update_cell(
                        VO_cell.row,
                        Total_Users_cell.col,
                        VOs_list[index]["total_members"],
                    )

                    if env["LOG"] == "DEBUG":
                        print(
                            colourise("green", "[LOG]"),
                            "Updated statistics (%s, %s, %s) for the VO [%s]"
                            % (
                                VOs_list[index]["users"],
                                VOs_list[index]["active_members"],
                                VOs_list[index]["total_members"],
                                VOs_list[index]["name"],
                            ),
                        )

                    # Remove the VO from the VOs_list
                    VOs_list.remove(VOs_list[index])

                index = index + 1
            except:
                print(
                    colourise("red", "[WARNING]"),
                    "Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'",
                )
                time.sleep(120)
                index = index - 1

    print(
        colourise("cyan", "[INFO]"),
        " Existing VOs statistics updated in the Google worksheet!",
    )

    # 2.) Insert new VO with its metrics in the worksheet
    print(
        colourise("cyan", "\n[INFO]"),
        "\tInsert *new VOs* and related statistics in the Google worksheet in progress..",
    )
    print("\tThis operation may take few minutes. Please wait!")

    index = 0
    # Identify the proper column ID for the VO
    col_index = get_GWorkSheet_HeaderPosition(env, worksheet, accounting_period)
    Registered_Users_index = get_GWorkSheet_HeaderPosition(
        env, worksheet, "Registered Users"
    )
    Total_Users_index = get_GWorkSheet_HeaderPosition(env, worksheet, "Total Users")

    while index < len(VOs_list):
        try:
            row_index = get_GWorkSheet_VOPosition(worksheet, VOs_list[index]["name"])
            print(
                "Insert the VO [%s] at: (%d, %d)"
                % (VOs_list[index]["name"], row_index, col_index)
            )

            # Insert a new row in the worksheet
            body = ["", ""]
            worksheet.insert_row(body, index=row_index)

            # Update the cells with the metadata
            worksheet.update_cell(row_index, 1, VOs_list[index]["name"])

            # Update the Google Worksheet cell (with the 'Num. of users' in the reporting period)
            worksheet.update_cell(row_index, col_index, VOs_list[index]["users"])

            # Update the Google Worksheet cell (with the 'Registered' users)
            worksheet.update_cell(
                row_index, Registered_Users_cell.col, VOs_list[index]["active_members"]
            )

            # Update the Google Worksheet cell (with the 'Total' users)
            worksheet.update_cell(
                row_index, Total_Users_cell.col, VOs_list[index]["total_members"]
            )

            print("Updated statistics for the VO [%s]" % VOs_list[index]["name"])

            index = index + 1

        except:
            print(
                colourise("red", "[WARNING]"),
                "Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'",
            )
            time.sleep(120)
            index = index - 1

    if len(VOs_list) > 0:
        print(
            colourise("cyan", "[INFO]"),
            " [%d] *new* VO statistics added in the Google worksheet!" % len(VOs_list),
        )


def main():
    dt = datetime.datetime.now()
    # Convert dt to string in dd-mm-yyyy HH:MM:SS
    timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")

    # Initialise the environment settings
    env = get_env_settings()
    print("\nLog Level = %s" % colourise("cyan", env["LOG"]))

    accounting_period = (
        env["DATE_FROM"][0:4] + "." + env["DATE_FROM"][-2:] + "-" + env["DATE_TO"][-2:]
    )
    print(colourise("cyan", "\n[INFO]"), "\tReporting Period: '%s'" % accounting_period)

    # Initialise the GWorkSheet
    worksheet = init_GWorkSheet(env)

    # Update the headers of the GWorkSheet (if necessary)
    update_GWorkSheet_Headers(env, worksheet, accounting_period)

    # Retrieve metadata for all the production VOs
    VOs_stats = get_VOs_stats(env)
    if env["LOG"] == "DEBUG":
        print(json.dumps(VOs_stats, indent=4))

    # Update the GWorkSheet
    update_GWorkSheet_VOs(env, worksheet, VOs_stats, accounting_period)

    # Update the timestamp of the last update
    worksheet.insert_note("A1", "Last Update on: " + timestamp)


if __name__ == "__main__":
    main()
