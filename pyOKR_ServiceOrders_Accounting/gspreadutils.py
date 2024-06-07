#!/usr/bin/env python3
#
#  Copyright 2024 EGI Foundation
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
import warnings

warnings.filterwarnings("ignore")
from utils import colourise, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.2"
__date__      = "$Date: 25/04/2024 11:58:27"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def init_GWorkSheet(env):
    ''' Initialise the GWorkSheet settings and return the worksheet '''

    worksheet = ""

    try:
        # Get the service account
        account = gspread.service_account(env['SERVICE_ACCOUNT_FILE'])

        # Open the GoogleSheet
        sheet = account.open(env['GOOGLE_SHEET_NAME'])

        # Open the Worksheet
        worksheet = sheet.worksheet(env['GOOGLE_SERVICE_ORDERS_WORKSHEET'])

    except FileNotFoundError as error:
        print(colourise("red", "[ABORT]"), \
              "The env['SERVICE_ACCOUNT_FILE'] setting was *NOT FOUND*")
        print("\tPlease check environmental settings and try again!")

    except gspread.exceptions.SpreadsheetNotFound as error:
        print(colourise("red", "[ABORT]"), \
              "The env['GOOGLE_SHEET_NAME'] setting was *NOT FOUND*")
        print("\tPlease check environmental settings and try again!")

    except gspread.exceptions.WorksheetNotFound as error:
        print(colourise("red", "[ABORT]"), \
              "The env['GOOGLE_SERVICE_ORDERS_WORKSHEET'] setting was *NOT FOUND*")
        print("\tPlease check environmental settings and try again!")

    return(worksheet)

