# pyOKR_VOs_CPUs_SLAs_Accounting

## Install the credentials of the Google Service Account

Install the JSON file downloaded when you created a Google Service Account and rename it as `service_account.json`

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

Ask [Giuseppe La Rocca](mailto:giuseppe.larocca@egi.eu) for a copy of this Google Service Account.


## Calculate the Cloud CPU/h consumed by active SLAs in the specific period

This python client generates the Cloud CPU/h of the active SLAs

Edit the `openrc.sh`, configure the `scope=cloud` and the specify the `ACCOUNTING_METRIC` to be calculated

```bash
#!/bin/bash

export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
export ACCOUNTING_SCOPE="cloud" # for Cloud Compute

# Available metrics (for scope=cloud): 
# 'sum_elap_processors', 'mem-GByte', 'vm_num', 'sum_elap', 'cost', 'net_in', 'net_out', 'disk', 'processors'
export ACCOUNTING_METRIC="sum_elap_processors"

# Available Local Job Selector: 'onlyinfrajobs', 'localinfrajobs', 'onlylocaljobs'
export ACCOUNTING_LOCAL_JOB_SELECTOR="onlyinfrajobs"

# Available vo_group_selector: 'egi'
export ACCOUNTING_VO_GROUP_SELECTOR="egi"

# Available Data Selector: 'JSON', 'CSV'
export ACCOUNTING_DATA_SELECTOR="JSON"

export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_SLAs_HTC_WORKSHEET="Accounting SLAs HTC CPU/h"
export GOOGLE_SLAs_CLOUD_WORKSHEET="Accounting SLAs Cloud CPU/h"

export GOOGLE_SLAs_SHEET_NAME="EGI_VOs_SLAs_OLAs_dashboard"
export GOOGLE_SLAs_WORKSHEET="SLAs"

export VOs_FILE="VOs.json"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"

export DATE_FROM="2024/04"
export DATE_TO="2024/06"
```

Source the environment settings and run the client

```bash
]$ source openrc.sh && python3 pyVOs_CPUs_SLAs_Accounting_v0.2.py

Log Level = DEBUG

[DEBUG] Environmental settings
{
    "ACCOUNTING_SERVER_URL": "https://accounting.egi.eu",
    "ACCOUNTING_SCOPE": "cloud",
    "ACCOUNTING_METRIC": "elap_processors",
    "ACCOUNTING_LOCAL_JOB_SELECTOR": "onlyinfrajobs",
    "ACCOUNTING_VO_GROUP_SELECTOR": "egi",
    "ACCOUNTING_DATA_SELECTOR": "JSON",
    "SERVICE_ACCOUNT_PATH": "/home/larocca/modules/APIs/OKR/pyOKR_VOs_CPUs_SLAs_Accounting/.config/",
    "SERVICE_ACCOUNT_FILE": "/home/larocca/modules/APIs/OKR/pyOKR_VOs_CPUs_SLAs_Accounting/.config/service_account.json",
    "GOOGLE_SHEET_NAME": "OKR_Reports",
    "GOOGLE_SLAs_CLOUD_WORKSHEET": "Accounting SLAs Cloud CPU/h",
    "GOOGLE_SLAs_HTC_WORKSHEET": "Accounting SLAs HTC CPU/h",
    "GOOGLE_SLAs_SHEET_NAME": "EGI_VOs_SLAs_OLAs_dashboard",
    "GOOGLE_SLAs_WORKSHEET": "SLAs",
    "VOs_FILE": "VOs.json",
    "LOG": "DEBUG",
    "DATE_FROM": "2024/04",
    "DATE_TO": "2024/06",
    "SSL_CHECK": "True"
}

[INFO] The accounting_period *ALREADY FOUND* in the gspread at row: 36 

[DEBUG] Downloading accounting records from the EGI Accouting Portal in progress...
	This operation may take few minutes to complete. Please wait!

[INFO]  Fetching the accounting records for the VO [BELLE] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2024/04/2024/06/custom-belle/onlyinfrajobs/JSON/ [{'2024': 1581.9997, 'id': 'NGI_FRANCE', 'Total': 1582, 'Percent': 100}, {'2024': 1582, 'id': 'Total', 'Total': 1582, 'Percent': ''}, {'2024': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_FRANCE'}, {'id': 'ylegend', '0': 2024, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Provider: NGI_FRANCE; CPU/h:   1,582
- Total Cloud CPU/h =   1,582
[INFO] The vo 'belle' is *already* in the gspread
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [BIOMED] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2024/04/2024/06/custom-biomed/onlyinfrajobs/JSON/ [{'2024': 124846.7438, 'id': 'NGI_FRANCE', 'Total': 124847, 'Percent': 100}, {'2024': 124847, 'id': 'Total', 'Total': 124847, 'Percent': ''}, {'2024': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_FRANCE'}, {'id': 'ylegend', '0': 2024, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Provider: NGI_FRANCE; CPU/h: 124,847
- Total Cloud CPU/h = 124,847
[INFO] The vo 'biomed' is *already* in the gspread
[INFO] Updated the total Cloud CPU/h for the VO

[..]

[REPORT]
- Cloud CPU/h consumed by the EGI Scientific Communities
- Reporting period = 2024/04 - 2024/06
- Total = 3,066,203 Cloud CPU/h
```

The VO statistics are updated in the Google worksheet `Accounting SLAs Cloud CPU/h`

## Calculate the HTC CPU/h consumed by active SLAs in the specific period

This python client generates the HTC CPU/h of the active SLAs

Edit the `openrc.sh`, configure the `scope=egi` and the specify the `ACCOUNTING_METRIC` to be calculated.

```bash
#!/bin/bash

export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
export ACCOUNTING_SCOPE="egi"  # for High-Throughput Compute

# Available metrics (for scope=grid):
# 'elap_processors', 'njobs', 'normcpu', 'sumcpu', 'normelap', 'normelap_processors', 'sumelap', 'cpueff'
export ACCOUNTING_METRIC="elap_processors"

# Available Local Job Selector: 'onlyinfrajobs', 'localinfrajobs', 'onlylocaljobs'
export ACCOUNTING_LOCAL_JOB_SELECTOR="onlyinfrajobs"

# Available vo_group_selector: 'egi'
export ACCOUNTING_VO_GROUP_SELECTOR="egi"

# Available Data Selector: 'JSON', 'CSV'
export ACCOUNTING_DATA_SELECTOR="JSON"

export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_SLAs_HTC_WORKSHEET="Accounting SLAs HTC CPU/h"
export GOOGLE_SLAs_CLOUD_WORKSHEET="Accounting SLAs Cloud CPU/h"

export GOOGLE_SLAs_SHEET_NAME="EGI_VOs_SLAs_OLAs_dashboard"
export GOOGLE_SLAs_WORKSHEET="SLAs"

export VOs_FILE="VOs.json"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"

export DATE_FROM="2024/04"
export DATE_TO="2024/06"
```

Source the environment settings and run the client

```bash
Log Level = DEBUG

[DEBUG] Environmental settings
{
    "ACCOUNTING_SERVER_URL": "https://accounting.egi.eu",
    "ACCOUNTING_SCOPE": "egi",
    "ACCOUNTING_METRIC": "elap_processors",
    "ACCOUNTING_LOCAL_JOB_SELECTOR": "onlyinfrajobs",
    "ACCOUNTING_VO_GROUP_SELECTOR": "egi",
    "ACCOUNTING_DATA_SELECTOR": "JSON",
    "SERVICE_ACCOUNT_PATH": "/home/larocca/modules/APIs/OKR/pyOKR_VOs_CPUs_SLAs_Accounting/.config/",
    "SERVICE_ACCOUNT_FILE": "/home/larocca/modules/APIs/OKR/pyOKR_VOs_CPUs_SLAs_Accounting/.config/service_account.json",
    "GOOGLE_SHEET_NAME": "OKR_Reports",
    "GOOGLE_SLAs_CLOUD_WORKSHEET": "Accounting SLAs Cloud CPU/h",
    "GOOGLE_SLAs_HTC_WORKSHEET": "Accounting SLAs HTC CPU/h",
    "GOOGLE_SLAs_SHEET_NAME": "EGI_VOs_SLAs_OLAs_dashboard",
    "GOOGLE_SLAs_WORKSHEET": "SLAs",
    "VOs_FILE": "VOs.json",
    "LOG": "DEBUG",
    "DATE_FROM": "2024/04",
    "DATE_TO": "2024/06",
    "SSL_CHECK": "True"
}

[INFO] The accounting_period *ALREADY FOUND* in the gspread at row: 36 

[DEBUG] Downloading accounting records from the EGI Accouting Portal in progress...
	This operation may take few minutes to complete. Please wait!

[INFO]  Fetching the accounting records for the VO [BIOMED] in progress...
https://accounting.egi.eu/egi/elap_processors/REGION/Year/2024/04/2024/06/custom-biomed/onlyinfrajobs/JSON/ [{'2024': 343659.9115, 'id': 'NGI_FRANCE', 'Total': 343660, 'Percent': 48.54}, {'2024': 2.3105, 'id': 'NGI_IBERGRID', 'Total': 2, 'Percent': 0}, {'2024': 0.2914, 'id': 'NGI_TR', 'Total': 0, 'Percent': 0}, {'2024': 360672.1892, 'id': 'NGI_UK', 'Total': 360672, 'Percent': 50.95}, {'2024': 3605.6213, 'id': 'Russia', 'Total': 3606, 'Percent': 0.51}, {'2024': 707940, 'id': 'Total', 'Total': 707940, 'Percent': ''}, {'2024': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_FRANCE', '1': 'NGI_IBERGRID', '2': 'NGI_TR', '3': 'NGI_UK', '4': 'Russia'}, {'id': 'ylegend', '0': 2024, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'elap_processors'}]
- Provider: NGI_FRANCE; CPU/h: 343,660
- Provider: NGI_IBERGRID; CPU/h:       2
- Provider: NGI_TR; CPU/h:       0
- Provider: NGI_UK; CPU/h: 360,672
- Provider: Russia; CPU/h:   3,606
- Total HTC CPU/h = 707,940
[INFO] The vo 'biomed' is *already* in the gspread
[INFO] Updated the total HTC CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [ENMR.EU] in progress...
https://accounting.egi.eu/egi/elap_processors/REGION/Year/2024/04/2024/06/custom-enmr.eu/onlyinfrajobs/JSON/ [{'2024': 38206.7719, 'id': 'NGI_DE', 'Total': 38207, 'Percent': 4.86}, {'2024': 84435.8123, 'id': 'NGI_FRANCE', 'Total': 84436, 'Percent': 10.74}, {'2024': 15064.3918, 'id': 'NGI_IT', 'Total': 15064, 'Percent': 1.92}, {'2024': 389238.8951, 'id': 'NGI_NL', 'Total': 389239, 'Percent': 49.49}, {'2024': 259528.1602, 'id': 'NGI_UK', 'Total': 259528, 'Percent': 33}, {'2024': 786474, 'id': 'Total', 'Total': 786474, 'Percent': ''}, {'2024': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_DE', '1': 'NGI_FRANCE', '2': 'NGI_IT', '3': 'NGI_NL', '4': 'NGI_UK'}, {'id': 'ylegend', '0': 2024, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'elap_processors'}]
- Provider: NGI_DE; CPU/h:  38,207
- Provider: NGI_FRANCE; CPU/h:  84,436
- Provider: NGI_IT; CPU/h:  15,064
- Provider: NGI_NL; CPU/h: 389,239
- Provider: NGI_UK; CPU/h: 259,528
- Total HTC CPU/h = 786,474
[INFO] The vo 'enmr.eu' is *already* in the gspread
[INFO] Updated the total HTC CPU/h for the VO

[REPORT]
- HTC CPU/h consumed by the EGI Scientific Communities
- Reporting period = 2024/04 - 2024/06
- Total = 1,494,414 HTC CPU/h
```

The VO statistics are updated in the Google worksheet `Accounting SLAs HTC CPU/h`

