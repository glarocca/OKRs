This python client generates statistics about the total of Cloud|HTC CPU/h of the production VOs registered in the <a href="https://operations-portal.egi.eu/">EGI Operations Portal</a>. 

## Calculate the Cloud CPU/h consumed in the specific period

Edit the `openrc.sh`, configure the `scope=cloud` and the specify the accounting metric to be calculated

```
[..]
export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
export ACCOUNTING_SCOPE="cloud" # for Cloud Compute

# Available metrics (for scope=cloud): 
# 'sum_elap_processors', 'mem-GByte', 'vm_num', 'sum_elap', 'cost', 'net_in', 'net_out', 'disk', 'processors'
export ACCOUNTING_METRIC="sum_elap_processors"

# Google Spreadsheet settings
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_CLOUD_WORKSHEET="Accounting Cloud CPU/h"

export DATE_FROM="2023/01"
export DATE_TO="2023/06"
```

Source the environment settings and run the client

```
]$ source openrc.sh && python3 pyVOs_CPUs_Accounting_v0.2.py 

Log Level = INFO

[INFO]     Reporting Period: 2020.01-06
[Cloud]    Total Cloud CPU/h = 12,050,254
[noVOCPUs] VOs with *no* accounting records (3)
[VOCPUs]   VOs with *accounting* records (47)
```
The VO statistics are updated in the Google worksheet `Accounting Cloud CPU/h`

## Calculate the HTC CPU/h consumed in the specific period

Edit the `openrc.sh` file and configure the `scope=egi`

```
[..]
export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
export ACCOUNTING_SCOPE="egi" # for HTC Compute

# Available metrics (for scope=grid):
# 'elap_processors', 'njobs', 'normcpu', 'sumcpu', 'normelap', 'normelap_processors', 'sumelap', 'cpueff'
export ACCOUNTING_METRIC="elap_processors"

# Google Spreadsheet settings
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_HTC_WORKSHEET="Accounting HTC CPU/h"

export DATE_FROM="2023/01"
export DATE_TO="2023/06"
```

Source the environment settings and run the client

```
]$ source openrc.sh && python3 pyVOs_CPUs_Accounting_v0.2.py 

Log Level = INFO

[INFO]     Reporting Period: 2020.01-06
[HTC]      Total HTC CPU/h = 2,677,303,881
[noVOCPUs] VOs with *no* accounting records (3)
[VOCPUs]   VOs with *accounting* records (60)
```

The VO statistics are updated in the Google worksheet `Accounting HTC CPU/h`
