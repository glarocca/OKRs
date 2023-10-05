#!/bin/bash

###################################################
# E G I ** A C C O U N T I N G ** S E T T I N G S #
###################################################
#export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
#export ACCOUNTING_SCOPE="cloud" # for Cloud Compute
#export ACCOUNTING_SCOPE="egi"  # for High-Throughput Compute

# Available metrics (for scope=cloud): 
# 'sum_elap_processors', 'mem-GByte', 'vm_num', 'sum_elap', 'cost', 'net_in', 'net_out', 'disk', 'processors'
#export ACCOUNTING_METRIC="sum_elap_processors"
# Available metrics (for scope=grid):
# 'elap_processors', 'njobs', 'normcpu', 'sumcpu', 'normelap', 'normelap_processors', 'sumelap', 'cpueff'
#export ACCOUNTING_METRIC="elap_processors"

# Available Local Job Selector: 'onlyinfrajobs', 'localinfrajobs', 'onlylocaljobs'
#export ACCOUNTING_LOCAL_JOB_SELECTOR="onlyinfrajobs"

# Available vo_group_selector: 'egi'
#export ACCOUNTING_VO_GROUP_SELECTOR="egi"

# Available Data Selector: 'JSON', 'CSV'
#export ACCOUNTING_DATA_SELECTOR="JSON"

export DATE_FROM="2020/01"
export DATE_TO="2020/03"

##################################################################
# E G I ** O P E R A T I O N S ** P O R T A L ** S E T T I N G S #
##################################################################
export OPERATIONS_SERVER_URL="https://operations-portal.egi.eu/api/"
export OPERATIONS_API_KEY="61ba1a4deec9c" 
export OPERATIONS_FORMAT="json"
export OPERATIONS_VO_LIST_PREFIX="vo-list"
export OPERATIONS_VO_ID_CARD_PREFIX="vo-idcard"
export OPERATIONS_VOS_REPORT_PREFIX="egi-reports"

#######################################################
# E G I ** J I R A ** P O R T A L **  S E T T I N G S #
#######################################################
#export JIRA_SERVER_URL="https://jira.egi.eu/"
#export JIRA_AUTH_TOKEN="MTMzNDkxMjYwNzg2OlGxzek1UQ0qIV0pa0c8yXk9BvAI"

# Project used for the Customers' complains
#export COMPLAINS_PROJECTKEY="EGIREQ"

# Project used for the VO SLA violations
#export VIOLATIONS_PROJECTKEY="IMSSLA"
#export ISSUETYPE="SLA Violation"
#export SLA_VIOLATIONS_URL="https://confluence.egi.eu/display/IMS/SLA+Violations"

# Project used for the Service Orders
#export SERVICE_ORDERS_PROJECTKEY="EOSCSO"
#export SERVICE_ORDERS_ISSUETYPE="Epic"
#export SERVICE_ORDERS_ISSUETYPE="Service order"

###########################################################
# G O O G L E ** S P R E A D S H E E T ** S E T T I N G S #
###########################################################
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
#export GOOGLE_CLOUD_WORKSHEET="Accounting Cloud CPU/h"
#export GOOGLE_HTC_WORKSHEET="Accounting HTC CPU/h"
export GOOGLE_VOS_WORKSHEET="VOs statistics (certs)"
#export GOOGLE_SERVICE_ORDERS_WORKSHEET="Service Orders"

############################################
# E G I ** G T M H U B  ** S E T T I N G S #
############################################
#export QUANTIVE_SERVER_URL="https://app.gtmhub.com"
#export ACCOUNT_ID="6145a3e658ee380001ad8264"
#export OWNER_ID="64400fd9d214877ecdb0850b"
#export OWNER_CONTACT="Giuseppe La Rocca"
#export OWNER_EMAIL="giuseppe.larocca@egi.eu"
#export TASK_ID="64a7e9c88e4dc27043f8be9d"
#export TASK_ID="64c38fe6a68b60115b34ed3f"
#export PARENT_ID="643e72491effd56675dcac69"
#export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2d0bWh1Yi5jb20vYXBwX21ldGFkYXRhL2FjY291bnRJZCI6IjYxNDVhM2U2NThlZTM4MDAwMWFkODI2NCIsImlhdCI6MTY4OTU5ODU5Niwic3ViIjoiYXV0aDB8NjQ0MDBmZDllNDhjMzc3YmU1NTQxZTE3In0.5NZIIBlhAkM8QUrZVX03P39VJAu-Z-RKasG42AMGO-0"

# ACTIONS to perform on the OKR tasks
# Possible options: LIST, GET, and MODIFY
# - LIST = List all the OKRs tasks
# - GET = Gets a task by its unique identifier (id)
# - UPDATE = Update existing OKR task
#export ACTION="LIST"
#export ACTION="GET"
#export ACTION="UPDATE"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"
