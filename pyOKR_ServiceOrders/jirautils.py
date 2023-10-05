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
import warnings

warnings.filterwarnings("ignore")
from datetime import date
from dateutil.parser import parse
from utils import colourise

__author__ = "Giuseppe LA ROCCA"
__email__ = "giuseppe.larocca@egi.eu"
__version__ = "$Revision: 0.4"
__date__ = "$Date: 29/09/2023 11:58:27"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__ = "Apache Licence v2.0"


def getServiceOrders(env, orders):
    """Return the list of Service Orders from the EOSC MarketPlace"""

    start = (env["DATE_FROM"].replace("/", "-")) + "-01"
    end = (env["DATE_TO"].replace("/", "-")) + "-01"

    _url = (
        env["JIRA_SERVER_URL"]
        + "rest/api/latest/search?jql=project%3D"
        + env["SERVICE_ORDERS_PROJECTKEY"]
        + "+AND+created+%3E%3D+"
        + start
        + "+AND+created+%3C%3D+"
        + end
        + "&maxResults%3D1000"
        + " ORDER BY key DESC, priority DESC, updated DESC"
    )

    headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env["JIRA_AUTH_TOKEN"],
    }

    # print(_url)
    curl = requests.get(url=_url, headers=headers)
    orders = curl.json()

    # print(json.dumps(orders['issues'], indent=4, sort_keys=False))
    return orders["issues"]


def getCustomersComplains(env, complains):
    """Return the list of Customer Complains"""

    _issues = []

    start = (env["DATE_FROM"].replace("/", "-")) + "-01"
    end = (env["DATE_TO"].replace("/", "-")) + "-01"

    _url = (
        env["JIRA_SERVER_URL"]
        + "rest/api/latest/search?jql=project="
        + env["COMPLAINS_PROJECTKEY"]
        + "&Complain=Yes"
        + "&created>="
        + start
        + "&created<="
        + end
        + "&maxResults=10000"
    )
    # + " ORDER BY priority DESC, updated DESC"

    headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env["JIRA_AUTH_TOKEN"],
    }

    curl = requests.get(url=_url, headers=headers)
    issues = curl.json()

    total = 0
    for issue in issues["issues"]:
        # print(issue)
        # customfield_12409 = Complain
        if issue["fields"]["customfield_12409"]:
            if "Yes" in (issue["fields"]["customfield_12409"]["value"]):
                _issues.append(issue["key"])
                total = total + 1

    if len(_issues):
        for issue in _issues:
            complains = getComplainDetails(env, issue, complains)

    return complains


def getComplainDetails(env, issue, complains):
    """Retrieve the details for a given customer complain (issue)"""

    _url = env["JIRA_SERVER_URL"] + "rest/api/latest/issue/" + issue

    headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env["JIRA_AUTH_TOKEN"],
    }

    curl = requests.get(url=_url, headers=headers)
    issue_details = curl.json()

    if issue_details["fields"]["status"]["name"]:
        _year = issue_details["fields"]["created"][0:4]
        _month = issue_details["fields"]["created"][5:7]

        if int(_year) == int(env["DATE_TO"][0:4]) and int(_month) <= int(
            env["DATE_TO"][5:7]
        ):
            complain = {
                "Issue": issue,
                "URL": env["JIRA_SERVER_URL"] + "browse/" + issue,
                "Status": issue_details["fields"]["status"]["name"].upper(),
                "Created": issue_details["fields"]["created"][0:10],
                "Priority": issue_details["fields"]["priority"]["name"].upper(),
                "Assignee": issue_details["fields"]["assignee"]["displayName"],
                "Email": issue_details["fields"]["assignee"]["emailAddress"],
                "Complain": issue_details["fields"]["customfield_12409"]["value"],
            }

            complains.append(complain)

    return complains


def getSLAViolations(env, violations):
    """Retrieve the SLA violations in the reporting period"""

    _issues = []

    start = (env["DATE_FROM"].replace("/", "-")) + "-01"
    end = (env["DATE_TO"].replace("/", "-")) + "-01"

    _url = (
        env["JIRA_SERVER_URL"]
        + "rest/api/latest/search?jql=project="
        + env["VIOLATIONS_PROJECTKEY"]
        + "&issueType="
        + env["ISSUETYPE"]
        + "&resolution=Unresolved"
        + "&created>="
        + start
        + "&created<="
        + end
        + " ORDER BY priority DESC, updated DESC"
    )

    headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env["JIRA_AUTH_TOKEN"],
    }

    curl = requests.get(url=_url, headers=headers)
    issues = curl.json()

    for issue in issues["issues"]:
        if env["ISSUETYPE"] in (issue["fields"]["issuetype"]["name"]):
            _issues.append(issue["key"])

    if len(_issues):
        for issue in _issues:
            violations = getSLAViolationsDetails(env, issue, violations)

    return violations


def getSLAViolationsDetails(env, issue, violations):
    """Retrieve the details for a given violation (issue)"""

    _url = env["JIRA_SERVER_URL"] + "rest/api/latest/issue/" + issue

    headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env["JIRA_AUTH_TOKEN"],
    }

    curl = requests.get(url=_url, headers=headers)
    issue_details = curl.json()

    if issue_details["fields"]["status"]["name"]:
        _year = issue_details["fields"]["created"][0:4]
        _month = issue_details["fields"]["created"][5:7]

        if int(_year) == int(env["DATE_TO"][0:4]) and int(_month) <= int(
            env["DATE_TO"][5:7]
        ):
            violation = {
                "Issue": issue,
                "URL": env["JIRA_SERVER_URL"] + "browse/" + issue,
                "Status": issue_details["fields"]["status"]["name"].upper(),
                "Created": issue_details["fields"]["created"][0:10],
                "Priority": issue_details["fields"]["priority"]["name"].upper(),
            }

            violations.append(violation)

    return violations
