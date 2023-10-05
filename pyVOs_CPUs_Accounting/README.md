# pyOKR_VOs_CPUs_Accounting

## Install the credenatials of the Google Service Account

Install the JSON file downloaded when you created a Google Service Account nd rename it as `service_account.json`

```bash
]$ mkdir $PWD/.config
]$ cat .config/service_account.json
{
  "type": "service_account",
  "project_id": "striped-rhino-395008",
  "private_key_id": "<ADD_PRIVATE_KEY_ID> HERE",
  "private_key": "<ADD PRIVATE_KEY> HERE",
  "client_email": "python-google-sheet-service-ac@striped-rhino-395008.iam.gserviceaccount.com",
  "client_id": "<ADD CLIENT_ID> HERE",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-google-sheet-service-ac%40striped-rhino-395008.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

## Calculate the Cloud CPU/h consumed in the specific period

This python client generates the Cloud CPU/h of the production VOs registered in the [EGI Operations Portal](https://operations-portal.egi.eu/)

Edit the `openrc.sh`, configure the `scope=cloud` and the specify the `ACCOUNTING_METRIC` to be calculated

```bash
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

```bash
]$ source openrc.sh && python3 pyVOs_CPUs_Accounting_v0.2.py

Log Level = INFO

[INFO]     Reporting Period: 2020.01-06
[Cloud]    Total Cloud CPU/h = 12,050,254
[noVOCPUs] VOs with *no* accounting records (3)
[VOCPUs]   VOs with *accounting* records (47)
```

The VO statistics are updated in the Google worksheet `Accounting Cloud CPU/h`

## Calculate the HTC CPU/h consumed in the specific period

This python client generates the HTC CPU/h of the production VOs registered in the [EGI Operations Portal](https://operations-portal.egi.eu/)

Edit the `openrc.sh`, configure the `scope=egi` and the specify the `ACCOUNTING_METRIC` to be calculated.

```bash
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

```bash
]$ source openrc.sh && python3 pyVOs_CPUs_Accounting_v0.2.py

Log Level = INFO

[INFO]     Reporting Period: 2020.01-06
[HTC]      Total HTC CPU/h = 2,677,303,881
[noVOCPUs] VOs with *no* accounting records (3)
[VOCPUs]   VOs with *accounting* records (60)
```

The VO statistics are updated in the Google worksheet `Accounting HTC CPU/h`
