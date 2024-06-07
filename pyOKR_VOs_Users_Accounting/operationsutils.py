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

import json
import requests
from utils import colourise, highlight, get_env_settings

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.9"
__date__      = "$Date: 06/11/2023 18:23:17"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__   = "Apache Licence v2.0"


def get_VOs_report(env):
    '''
        Returns reports of the list of VOs created and deleted in the reporting period
        Endpoint:
         * `/egi-reports/vo`
    '''

    start = (env['DATE_FROM'].replace("/", "-")) + "-01"
    end = (env['DATE_TO'].replace("/", "-")) + "-01"

    headers = {
         "Accept": "Application/json",
         "X-API-Key": env['OPERATIONS_API_KEY']
    }

    _url = env['OPERATIONS_SERVER_URL'] \
        + env['OPERATIONS_VOS_REPORT_PREFIX'] \
        + "/vo?" \
        + "start_date=" + start \
        + "&end_date=" + end \
        + "&format=json"


    if env['SSL_CHECK'] == "False":
       curl = requests.get(url=_url, headers=headers, verify=False)
    else:
       curl = requests.get(url=_url, headers=headers)

    response = curl.json()
    VOs_report = []

    if response:
       for item in response['report']:
            vos = []
            for vo_list in item['vos']:
                if "Pending" in item['status']:
                    tmp = ' '.join(vo_list['vo']) + "(PE)"
                if "Deleted" in item['status']:
                    tmp = ' '.join(vo_list['vo']) + "(D)"
                if "Leaving" in item['status']:
                    tmp = ' '.join(vo_list['vo']) + "(L)"
                if "Production" in item['status']:
                    tmp = ' '.join(vo_list['vo']) + "(P)"
                vos.append(tmp)
            
            VOs_report.append({
                "status": item['status'],
                "count": item['count'],
                "vos": vos
            })

    return(VOs_report)
    

def get_VO_metadata(index, env, vo_name):
    '''
        Returns the 'acknowldegement' and the 'publicationUrl' metadata for a given VO
        Endpoint:
         * `/vo-idcard/{vo_name}/{_format}`
    '''

    headers = {
         "Accept": "Application/json",
         "X-API-Key": env['OPERATIONS_API_KEY']
    }

    publicationsURL = ""
    statement = ""

    _url = env['OPERATIONS_SERVER_URL'] \
            + env['OPERATIONS_VO_ID_CARD_PREFIX'] \
            + "/" + vo_name + "/" + env['OPERATIONS_FORMAT']
 
    if env['SSL_CHECK'] == "False":
       curl = requests.get(url=_url, headers=headers, verify=False)
    else:   
       curl = requests.get(url=_url, headers=headers)
    response = curl.json()

    if response:
       for details in response['data']:
           for VO_details in details['Vo'][6]['VoAcknowledgments']:
               
               if VO_details['VoAcknowledgment'][1]['acknowledgment']:
                  statement = VO_details['VoAcknowledgment'][1]['acknowledgment']
               else:
                  statement = "N/A"

               if VO_details['VoAcknowledgment'][3]['publicationUrl']:
                  publicationsURL = VO_details['VoAcknowledgment'][3]['publicationUrl']
               else:
                  publicationsURL = "N/A"

    return statement, publicationsURL, index


def get_VO_stats(env, vo):
    '''
       Returns the statistics of the production VO with minimal information:
        - name,
        - scope,
        - homepage,
        - num. of members,
        - acknowledgement,
        - publications url

       Endpoint:
         * `/vo-list/{_format}`
    '''

    headers = {
         "Accept": "Application/json",
         "X-API-Key": env['OPERATIONS_API_KEY']
    }

    _url = env['OPERATIONS_SERVER_URL'] \
            + env['OPERATIONS_VO_LIST_PREFIX'] \
            + "/" + env['OPERATIONS_FORMAT']


    # Initialize the list
    vo_stats = []
    index = 0

    # Fetches the production VOs from the EGI Operations Portal
    if env['SSL_CHECK'] == "False":
       curl = requests.get(url=_url, headers=headers, verify=False)
    else:   
       curl = requests.get(url=_url, headers=headers)

    response = curl.json()

    if response:
        for details in response['data']:
            if vo in details['name']:

               statement, publicationsURL, index = get_VO_metadata(
                    index,
                    env,
                    details['name']) 
              
               if details['members'] == "0.0":
                  details['members'] = "0"
               
               if details['membersTotal'] == "0.0":
                  details['membersTotal'] = "0"

               # Append the VO details in the vo_details list
               vo_stats.append(
                    {"name": details['name'],
                     "scope": details['scope'],
                     "url": details['homeUrl'],
                     "users": get_VO_users(env, details['name']), # Current users in the VO 
                     "active_members": details['members'], # Active users in the VO
                     "total_members" : details['membersTotal'], # Total users in the VO
                     "acknowledgement": statement,
                     "publicationsURL": publicationsURL})
               #print(json.dumps(vo_stats, indent=4))

            index = index + 1 

    return(vo_stats)


def get_VOs_stats(env):
    '''
       Returns the list of productions VOs with minimal information:
        - name,
        - scope,
        - homepage,
        - num. of members,
        - acknowledgement,
        - publications url

       Endpoint:
         * `/vo-list/{_format}`
    '''

    headers = {
         "Accept": "Application/json",
         "X-API-Key": env['OPERATIONS_API_KEY']
    }

    _url = env['OPERATIONS_SERVER_URL'] \
            + env['OPERATIONS_VO_LIST_PREFIX'] \
            + "/" + env['OPERATIONS_FORMAT']

    # Initialize the list
    vo_details = []
    index = 0

    # Fetches the production VOs from the EGI Operations Portal
    if env['SSL_CHECK'] == "False":
       curl = requests.get(url=_url, headers=headers, verify=False)
    else:   
       curl = requests.get(url=_url, headers=headers)

    response = curl.json()

    if response:
        print(colourise("cyan", "\n[INFO]"), \
                "\tDownloading the VOs metadata from the EGI Operations Portal in progress..")
        print("\tThis operation may take few minutes. Please wait!\n")

        for details in response['data']:
            if env['LOG'] == "DEBUG":
               print(colourise("green", "\n[LOG]"), \
               "[%d] Fetching metadata for the VO [%s] in progress.." %(index, details['name']))
            else:   
               print(colourise("green", "\n[LOG]"), \
               "[%d] Fetching metadata for the VO [%s] in progress.." %(index, details['name']))
            #print(json.dumps(details, indent=4))

            statement, publicationsURL, index = get_VO_metadata(
                    index,
                    env,
                    details['name'])

            if details['members'] == "0.0":
               details['members'] = "0"

            if details['membersTotal'] == "0.0":
               details['membersTotal'] = "0"

            # Append the VO details in the vo_details list
            if statement and publicationsURL:
               
               vo_detail = {
                  "name": details['name'],
                  "scope": details['scope'],
                  "url": details['homeUrl'],
                  "users": get_VO_users(env, details['name']),    
                  "active_members": details['members'], # Active users in the VO
                  "total_members" : details['membersTotal'], # Total users in the VO
                  "acknowledgement": statement,
                  "publicationsURL": publicationsURL
               }
            else:  
                vo_detail = {
                  "name": details['name'],
                  "scope": details['scope'],
                  "url": details['homeUrl'],
                  "users": get_VO_users(env, details['name']),
                  "active_members": details['members'], # Active users in the VO
                  "total_members" : details['membersTotal'], # Total users in the VO
                  "acknowledgement": "N/A",
                  "publicationsURL": "N/A"
               }

            if env['LOG'] == "DEBUG":
                print(json.dumps(vo_detail, indent=4))

            vo_details.append(vo_detail)    
            
            index = index + 1 

    return(vo_details)


def get_VO_users(env, vo):
    '''
       Returns the num. of users of the production VO in the specific period
       Endpoint:
         * `/egi-reports/vo-users?start_date=YYYY-MM&end_date=YYYY-MM&format={_format}&vo={_voname}`
    '''

    headers = {
         "Accept": "Application/json",
         "X-API-Key": env['OPERATIONS_API_KEY']
    }

    _url = env['OPERATIONS_SERVER_URL'] \
            + env['OPERATIONS_VOS_REPORT_PREFIX'] \
            + "/vo-users?start_date=" + env['DATE_FROM'].replace("/","-") \
            + "&end_date=" + env['DATE_TO'].replace("/","-") \
            + "&format=" + env['OPERATIONS_FORMAT'] \
            + "&vo=" + vo

    # Fetches the production VOs from the EGI Operations Portal
    if env['SSL_CHECK'] == "False":
       curl = requests.get(url=_url, headers=headers, verify=False)
    else:
       curl = requests.get(url=_url, headers=headers)

    users = "0"
    if (curl.status_code == 200):
        try:
           response = curl.json()
           
           if response['users'] is not None:
              users = response['users'][0]['total']
              
              for key in response['users']:
                  # Iterate over the dictionary (keys = month, total, nbadded, nbremoved)
                  metadata = {
                    "month": key['month'],
                    "total": key['total'],
                    "added": key['nbadded'],
                    "removed": key['nbremoved']
                  }
                  print(metadata)
            
              #Print the number of users in the VO
              #print(users)
 
        except (requests.exceptions.JSONDecodeError, KeyError):
             pass
    
    return(users)    


