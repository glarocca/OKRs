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

import configparser
import os
import string

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.7"
__date__      = "$Date: 05/09/2023 11:58:27"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__   = "Apache Licence v2.0"



def colourise(colour, text):
    ''' Colourise - colours text in shell. '''
    ''' Returns plain if colour doesn't exist '''

    if colour == "black":
        return "\033[1;30m" + str(text) + "\033[1;m"
    if colour == "red":
        return "\033[1;31m" + str(text) + "\033[1;m"
    if colour == "green":
        return "\033[1;32m" + str(text) + "\033[1;m"
    if colour == "yellow":
        return "\033[1;33m" + str(text) + "\033[1;m"
    if colour == "blue":
        return "\033[1;34m" + str(text) + "\033[1;m"
    if colour == "magenta":
        return "\033[1;35m" + str(text) + "\033[1;m"
    if colour == "cyan":
        return "\033[1;36m" + str(text) + "\033[1;m"
    if colour == "gray":
        return "\033[1;37m" + str(text) + "\033[1;m"
    return str(text)


def highlight(colour, text):
    ''' Highlight - highlights text in shell. '''
    ''' Returns plain if colour doesn't exist. '''

    if colour == "black":
        return "\033[1;40m" + str(text) + "\033[1;m"
    if colour == "red":
        return "\033[1;41m" + str(text) + "\033[1;m"
    if colour == "green":
        return "\033[1;42m" + str(text) + "\033[1;m"
    if colour == "yellow":
        return "\033[1;43m" + str(text) + "\033[1;m"
    if colour == "blue":
        return "\033[1;44m" + str(text) + "\033[1;m"
    if colour == "magenta":
        return "\033[1;45m" + str(text) + "\033[1;m"
    if colour == "cyan":
        return "\033[1;46m" + str(text) + "\033[1;m"
    if colour == "gray":
        return "\033[1;47m" + str(text) + "\033[1;m"
    return str(text)


def get_env_settings():
        ''' Reading profile settings from env '''

        d = {}
        try:
           # EGI Operations Portal settings 
           d['OPERATIONS_SERVER_URL'] = os.environ['OPERATIONS_SERVER_URL']
           d['OPERATIONS_API_KEY'] = os.environ['OPERATIONS_API_KEY']
           d['OPERATIONS_FORMAT'] = os.environ['OPERATIONS_FORMAT']
           d['OPERATIONS_VO_LIST_PREFIX'] = os.environ['OPERATIONS_VO_LIST_PREFIX']
           d['OPERATIONS_VO_ID_CARD_PREFIX'] = os.environ['OPERATIONS_VO_ID_CARD_PREFIX']
           d['OPERATIONS_VOS_REPORT_PREFIX'] = os.environ['OPERATIONS_VOS_REPORT_PREFIX']
          
           # Google sheet settings
           d['SERVICE_ACCOUNT_PATH'] = os.environ['SERVICE_ACCOUNT_PATH']
           d['SERVICE_ACCOUNT_FILE'] = os.environ['SERVICE_ACCOUNT_FILE']
           d['GOOGLE_SHEET_NAME'] = os.environ['GOOGLE_SHEET_NAME']
           d['GOOGLE_CLOUD_WORKSHEET'] = os.environ['GOOGLE_CLOUD_WORKSHEET']
           d['GOOGLE_HTC_WORKSHEET'] = os.environ['GOOGLE_HTC_WORKSHEET']
           d['GOOGLE_VOS_WORKSHEET'] = os.environ['GOOGLE_VOS_WORKSHEET']

           # Generic settings
           d['LOG'] = os.environ['LOG']
           d['DATE_FROM'] = os.environ['DATE_FROM']
           d['DATE_TO'] = os.environ['DATE_TO']
           d['SSL_CHECK'] = os.environ['SSL_CHECK']

        except:
          print(colourise("red", "ERROR: os.environment settings not found!"))
        
        return d
