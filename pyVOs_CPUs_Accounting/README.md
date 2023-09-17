## Configure the settings

Edit and export the settings:

```
]$ cat openrc.sh 
#!/bin/bash

###################################################
# E G I ** A C C O U N T I N G ** S E T T I N G S #
###################################################
export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
#export ACCOUNTING_SCOPE="cloud" # for Cloud Compute
export ACCOUNTING_SCOPE="egi"  # for High-Throughput Compute

# Available metrics (for scope=cloud): 
# 'sum_elap_processors', 'mem-GByte', 'vm_num', 'sum_elap', 'cost', 'net_in', 'net_out', 'disk', 'processors'
#export ACCOUNTING_METRIC="sum_elap_processors"

# Available metrics (for scope=grid):
# 'elap_processors', 'njobs', 'normcpu', 'sumcpu', 'normelap', 'normelap_processors', 'sumelap', 'cpueff'
export ACCOUNTING_METRIC="elap_processors"

# Available Local Job Selector: 'onlyinfrajobs', 'localinfrajobs', 'onlylocaljobs'
export ACCOUNTING_LOCAL_JOB_SELECTOR="onlyinfrajobs"

# Available vo_group_selector: 'egi'
export ACCOUNTING_VO_GROUP_SELECTOR="egi"

# Available Data Selector: 'JSON', 'CSV'
export ACCOUNTING_DATA_SELECTOR="JSON"

export DATE_FROM="2023/01"
export DATE_TO="2023/06"

##################################################################
# E G I ** O P E R A T I O N S ** P O R T A L ** S E T T I N G S #
##################################################################
export OPERATIONS_SERVER_URL="https://operations-portal.egi.eu/api/"
export OPERATIONS_API_KEY="*************" 
export OPERATIONS_FORMAT="json"
export OPERATIONS_VO_LIST_PREFIX="vo-list"
export OPERATIONS_VO_ID_CARD_PREFIX="vo-idcard"
export OPERATIONS_VOS_REPORT_PREFIX="egi-reports"

###########################################################
# G O O G L E ** S P R E A D S H E E T ** S E T T I N G S #
###########################################################
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_CLOUD_WORKSHEET="Accounting Cloud CPU/h"
export GOOGLE_HTC_WORKSHEET="Accounting HTC CPU/h"
export GOOGLE_VOS_WORKSHEET="VOs statistics"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
```

