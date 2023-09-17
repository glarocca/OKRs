#!/bin/bash

###################################################
# E G I ** A C C O U N T I N G ** S E T T I N G S #
###################################################
export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
export ACCOUNTING_SCOPE="cloud" # for Cloud Compute
#export ACCOUNTING_SCOPE="egi"  # for High-Throughput Compute

# Available metrics (for scope=cloud): 
# 'sum_elap_processors', 'mem-GByte', 'vm_num', 'sum_elap', 'cost', 'net_in', 'net_out', 'disk', 'processors'
export ACCOUNTING_METRIC="sum_elap_processors"

# Available metrics (for scope=grid):
# 'elap_processors', 'njobs', 'normcpu', 'sumcpu', 'normelap', 'normelap_processors', 'sumelap', 'cpueff'
#export ACCOUNTING_METRIC="elap_processors"

# Available Local Job Selector: 'onlyinfrajobs', 'localinfrajobs', 'onlylocaljobs'
export ACCOUNTING_LOCAL_JOB_SELECTOR="onlyinfrajobs"

# Available vo_group_selector: 'egi'
export ACCOUNTING_VO_GROUP_SELECTOR="egi"

# Available Data Selector: 'JSON', 'CSV'
export ACCOUNTING_DATA_SELECTOR="JSON"

export DATE_FROM="2020/01"
export DATE_TO="2020/06"

###########################################################
# G O O G L E ** S P R E A D S H E E T ** S E T T I N G S #
###########################################################
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_CLOUD_WORKSHEET="Accounting Cloud CPU/h"
export GOOGLE_HTC_WORKSHEET="Accounting HTC CPU/h"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
