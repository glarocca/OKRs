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
export GOOGLE_OLAs_WORKSHEET="OLAs"

export ACTIVE_SLAs_FILE="VOs.json"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"

export DATE_FROM="2025/01"
export DATE_TO="2025/02"
```

Source the environment settings and run the client

```bash
]$ source openrc.sh && python3 pyVOs_CPUs_SLAs_Accounting_v0.4.py

Log Level = DEBUG

[DEBUG] Environmental settings
{
    "ACCOUNTING_SERVER_URL": "https://accounting.egi.eu",
    "ACCOUNTING_SCOPE": "cloud",
    "ACCOUNTING_METRIC": "sum_elap_processors",
    "ACCOUNTING_LOCAL_JOB_SELECTOR": "onlyinfrajobs",
    "ACCOUNTING_VO_GROUP_SELECTOR": "egi",
    "ACCOUNTING_DATA_SELECTOR": "JSON",
    "SERVICE_ACCOUNT_PATH": "/home/larocca/modules/APIs/OKRs/pyOKR_VOs_CPUs_SLAs_Accounting/.config/",
    "SERVICE_ACCOUNT_FILE": "/home/larocca/modules/APIs/OKRs/pyOKR_VOs_CPUs_SLAs_Accounting/.config/service_account.json",
    "GOOGLE_SHEET_NAME": "OKR_Reports",
    "GOOGLE_SLAs_CLOUD_WORKSHEET": "Accounting SLAs Cloud CPU/h",
    "GOOGLE_SLAs_HTC_WORKSHEET": "Accounting SLAs HTC CPU/h",
    "GOOGLE_SLAs_SHEET_NAME": "EGI_VOs_SLAs_OLAs_dashboard",
    "GOOGLE_SLAs_WORKSHEET": "SLAs",
    "GOOGLE_OLAs_WORKSHEET": "OLAs",
    "ACTIVE_SLAs_FILE": "VOs.json",
    "LOG": "DEBUG",
    "DATE_FROM": "2025/01",
    "DATE_TO": "2025/02",
    "SSL_CHECK": "True"
}

[INFO]  Retrieve metadata of running SLAs in progress...

[DEBUG] Fetching the active *SLAs* in progress...
	This operation may take few minutes to complete. Please wait!

[INFO] The accounting_period *ALREADY FOUND* in the gspread at row: 38 

[DEBUG] Downloading accounting records from the EGI Accouting Portal in progress...
	This operation may take few minutes to complete. Please wait!

[INFO]  Fetching the accounting records for the VO [BELLE] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-belle/onlyinfrajobs/JSON/ [{'2025': 1902.5622, 'id': 'NGI_FRANCE', 'Total': 1903, 'Percent': 100}, {'2025': 1903, 'id': 'Total', 'Total': 1903, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_FRANCE'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_FRANCE; CPU/h:   1,903
- Total Cloud CPU/h =   1,903
[INFO] The vo 'belle' is *already* in the gspread at position: 2
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.DECIDO-PROJECT.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.decido-project.eu/onlyinfrajobs/JSON/ [{'2025': 38640.0078, 'id': 'NGI_IT', 'Total': 38640, 'Percent': 100}, {'2025': 38640, 'id': 'Total', 'Total': 38640, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_IT'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_IT; CPU/h:  38,640
- Total Cloud CPU/h =  38,640
[INFO] The vo 'vo.decido-project.eu' is *already* in the gspread at position: 12
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [EISCAT.SE] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-eiscat.se/onlyinfrajobs/JSON/ [{'2025': 24593.2034, 'id': 'NGI_CHINA', 'Total': 24593, 'Percent': 77.82}, {'2025': 7008, 'id': 'NGI_TR', 'Total': 7008, 'Percent': 22.18}, {'2025': 31601, 'id': 'Total', 'Total': 31601, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CHINA', '1': 'NGI_TR'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CHINA; CPU/h:  24,593
- Resource Centre: NGI_TR; CPU/h:   7,008
- Total Cloud CPU/h =  31,601
[INFO] The vo 'eiscat.se' is *already* in the gspread at position: 4
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.EMPHASISPROJECT.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.emphasisproject.eu/onlyinfrajobs/JSON/ [{'2025': 65904.9705, 'id': 'NGI_CZ', 'Total': 65905, 'Percent': 100}, {'2025': 65905, 'id': 'Total', 'Total': 65905, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h:  65,905
- Total Cloud CPU/h =  65,905
[INFO] The vo 'vo.emphasisproject.eu' is *already* in the gspread at position: 14
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.ENVRIHUB.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.envrihub.eu/onlyinfrajobs/JSON/ [{'2025': 15240.78, 'id': 'NGI_CZ', 'Total': 15241, 'Percent': 100}, {'2025': 15241, 'id': 'Total', 'Total': 15241, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h:  15,241
- Total Cloud CPU/h =  15,241
[INFO] The vo 'vo.envrihub.eu' is *already* in the gspread at position: 17
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.USEGALAXY.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.usegalaxy.eu/onlyinfrajobs/JSON/ [{'2025': 110400.0222, 'id': 'NGI_IT', 'Total': 110400, 'Percent': 50.3}, {'2025': 67017.3495, 'id': 'NGI_SK', 'Total': 67017, 'Percent': 30.54}, {'2025': 42048, 'id': 'NGI_TR', 'Total': 42048, 'Percent': 19.16}, {'2025': 219465, 'id': 'Total', 'Total': 219465, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_IT', '1': 'NGI_SK', '2': 'NGI_TR'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_IT; CPU/h: 110,400
- Resource Centre: NGI_SK; CPU/h:  67,017
- Resource Centre: NGI_TR; CPU/h:  42,048
- Total Cloud CPU/h = 219,465
[INFO] The vo 'vo.usegalaxy.eu' is *already* in the gspread at position: 30
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.GEOSS.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.geoss.eu/onlyinfrajobs/JSON/ [{'2025': 84932.7946, 'id': 'NGI_CZ', 'Total': 84933, 'Percent': 100}, {'2025': 84933, 'id': 'Total', 'Total': 84933, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h:  84,933
- Total Cloud CPU/h =  84,933
[INFO] The vo 'vo.geoss.eu' is *already* in the gspread at position: 20
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [ICECUBE] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-icecube/onlyinfrajobs/JSON/ [{'2025': 88319.9822, 'id': 'NGI_CZ', 'Total': 88320, 'Percent': 100}, {'2025': 88320, 'id': 'Total', 'Total': 88320, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h:  88,320
- Total Cloud CPU/h =  88,320
[INFO] The vo 'icecube' is *already* in the gspread at position: 7
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [BIOMED] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-biomed/onlyinfrajobs/JSON/ [{'2025': 100588.64, 'id': 'NGI_FRANCE', 'Total': 100589, 'Percent': 100}, {'2025': 100589, 'id': 'Total', 'Total': 100589, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_FRANCE'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_FRANCE; CPU/h: 100,589
- Total Cloud CPU/h = 100,589
[INFO] The vo 'biomed' is *already* in the gspread at position: 3
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.EUROSEA.MARINE.IE] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.eurosea.marine.ie/onlyinfrajobs/JSON/ [{'2025': 7679.9972, 'id': 'NGI_IE', 'Total': 7680, 'Percent': 100}, {'2025': 7680, 'id': 'Total', 'Total': 7680, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_IE'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_IE; CPU/h:   7,680
- Total Cloud CPU/h =   7,680
[INFO] The vo 'vo.eurosea.marine.ie' is *already* in the gspread at position: 19
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.NEURODESK.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.neurodesk.eu/onlyinfrajobs/JSON/ [{'2025': 80209.8356, 'id': 'NGI_CZ', 'Total': 80210, 'Percent': 100}, {'2025': 80210, 'id': 'Total', 'Total': 80210, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h:  80,210
- Total Cloud CPU/h =  80,210
[INFO] The vo 'vo.neurodesk.eu' is *already* in the gspread at position: 25
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.OBSEA.ES] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.obsea.es/onlyinfrajobs/JSON/ [{'2025': 49019.9789, 'id': 'NGI_IBERGRID', 'Total': 49020, 'Percent': 100}, {'2025': 49020, 'id': 'Total', 'Total': 49020, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_IBERGRID'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_IBERGRID; CPU/h:  49,020
- Total Cloud CPU/h =  49,020
[INFO] The vo 'vo.obsea.es' is *already* in the gspread at position: 24
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.OPERAS-EU.ORG] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.operas-eu.org/onlyinfrajobs/JSON/ [{'2025': 57778.2861, 'id': 'NGI_FRANCE', 'Total': 57778, 'Percent': 100}, {'2025': 57778, 'id': 'Total', 'Total': 57778, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_FRANCE'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_FRANCE; CPU/h:  57,778
- Total Cloud CPU/h =  57,778
[INFO] The vo 'vo.operas-eu.org' is *already* in the gspread at position: 26
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.PANGEO.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.pangeo.eu/onlyinfrajobs/JSON/ [{'2025': 287133.9778, 'id': 'NGI_CZ', 'Total': 287134, 'Percent': 100}, {'2025': 287134, 'id': 'Total', 'Total': 287134, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h: 287,134
- Total Cloud CPU/h = 287,134
[INFO] The vo 'vo.pangeo.eu' is *already* in the gspread at position: 28
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.RADIOTRACERS4PSMA.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.radiotracers4psma.eu/onlyinfrajobs/JSON/ [{'2025': 88319.9822, 'id': 'NGI_CZ', 'Total': 88320, 'Percent': 100}, {'2025': 88320, 'id': 'Total', 'Total': 88320, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h:  88,320
- Total Cloud CPU/h =  88,320
[INFO] The vo 'vo.radiotracers4psma.eu' is *already* in the gspread at position: 29
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [ENMR.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-enmr.eu/onlyinfrajobs/JSON/ [{'2025': 2413.5845, 'id': 'NGI_CHINA', 'Total': 2414, 'Percent': 91.34}, {'2025': 229.3667, 'id': 'NGI_CZ', 'Total': 229, 'Percent': 8.66}, {'2025': 2643, 'id': 'Total', 'Total': 2643, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CHINA', '1': 'NGI_CZ'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CHINA; CPU/h:   2,414
- Resource Centre: NGI_CZ; CPU/h:     229
- Total Cloud CPU/h =   2,643
[INFO] The vo 'enmr.eu' is *already* in the gspread at position: 5
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [VO.ACCESS.EGI.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-vo.access.egi.eu/onlyinfrajobs/JSON/ [{'2025': 1380, 'id': 'AfricaArabia', 'Total': 1380, 'Percent': 0.58}, {'2025': 2903.9994, 'id': 'NGI_CHINA', 'Total': 2904, 'Percent': 1.21}, {'2025': 96515.2705, 'id': 'NGI_DE', 'Total': 96515, 'Percent': 40.23}, {'2025': 60034.7798, 'id': 'NGI_FRANCE', 'Total': 60035, 'Percent': 25.03}, {'2025': 1535.9994, 'id': 'NGI_IE', 'Total': 1536, 'Percent': 0.64}, {'2025': 34559.7377, 'id': 'NGI_SK', 'Total': 34560, 'Percent': 14.41}, {'2025': 38831.1088, 'id': 'NGI_TR', 'Total': 38831, 'Percent': 16.19}, {'2025': 4137.0009, 'id': 'NGI_UA', 'Total': 4137, 'Percent': 1.72}, {'2025': 239898, 'id': 'Total', 'Total': 239898, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'AfricaArabia', '1': 'NGI_CHINA', '2': 'NGI_DE', '3': 'NGI_FRANCE', '4': 'NGI_IE', '5': 'NGI_SK', '6': 'NGI_TR', '7': 'NGI_UA'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: AfricaArabia; CPU/h:   1,380
- Resource Centre: NGI_CHINA; CPU/h:   2,904
- Resource Centre: NGI_DE; CPU/h:  96,515
- Resource Centre: NGI_FRANCE; CPU/h:  60,035
- Resource Centre: NGI_IE; CPU/h:   1,536
- Resource Centre: NGI_SK; CPU/h:  34,560
- Resource Centre: NGI_TR; CPU/h:  38,831
- Resource Centre: NGI_UA; CPU/h:   4,137
- Total Cloud CPU/h = 239,898
[INFO] The vo 'vo.access.egi.eu' is *already* in the gspread at position: 32
[INFO] Updated the total Cloud CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [TRAINING.EGI.EU] in progress...
https://accounting.egi.eu/cloud/sum_elap_processors/REGION/Year/2025/01/2025/02/custom-training.egi.eu/onlyinfrajobs/JSON/ [{'2025': 13807.9, 'id': 'NGI_CZ', 'Total': 13808, 'Percent': 99.95}, {'2025': 6.6717, 'id': 'NGI_SK', 'Total': 7, 'Percent': 0.05}, {'2025': 13815, 'id': 'Total', 'Total': 13815, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_CZ', '1': 'NGI_SK'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'sum_elap_processors'}]
- Resource Centre: NGI_CZ; CPU/h:  13,808
- Resource Centre: NGI_SK; CPU/h:       7
- Total Cloud CPU/h =  13,815
[INFO] The vo 'training.egi.eu' is *already* in the gspread at position: 33
[INFO] Updated the total Cloud CPU/h for the VO

[REPORT]
- Cloud CPU/h consumed by the EGI SLAs
- Reporting period = 2025/01 - 2025/02
- Total = 1,473,095 Cloud CPU/h
[INFO] Updated the total Cloud CPU/h for the VO
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
export GOOGLE_OLAs_WORKSHEET="OLAs"

export ACTIVE_SLAs_FILE="VOs.json"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"

export DATE_FROM="2025/01"
export DATE_TO="2025/02"
```

Source the environment settings and run the client

```bash
]$ source openrc.sh && python3 pyOKR_VOs_CPUs_SLAs_Accounting_v0.4.py 

Log Level = DEBUG

[DEBUG] Environmental settings
{
    "ACCOUNTING_SERVER_URL": "https://accounting.egi.eu",
    "ACCOUNTING_SCOPE": "egi",
    "ACCOUNTING_METRIC": "elap_processors",
    "ACCOUNTING_LOCAL_JOB_SELECTOR": "onlyinfrajobs",
    "ACCOUNTING_VO_GROUP_SELECTOR": "egi",
    "ACCOUNTING_DATA_SELECTOR": "JSON",
    "SERVICE_ACCOUNT_PATH": "/home/larocca/modules/APIs/OKRs/pyOKR_VOs_CPUs_SLAs_Accounting/.config/",
    "SERVICE_ACCOUNT_FILE": "/home/larocca/modules/APIs/OKRs/pyOKR_VOs_CPUs_SLAs_Accounting/.config/service_account.json",
    "GOOGLE_SHEET_NAME": "OKR_Reports",
    "GOOGLE_SLAs_CLOUD_WORKSHEET": "Accounting SLAs Cloud CPU/h",
    "GOOGLE_SLAs_HTC_WORKSHEET": "Accounting SLAs HTC CPU/h",
    "GOOGLE_SLAs_SHEET_NAME": "EGI_VOs_SLAs_OLAs_dashboard",
    "GOOGLE_SLAs_WORKSHEET": "SLAs",
    "GOOGLE_OLAs_WORKSHEET": "OLAs",
    "ACTIVE_SLAs_FILE": "VOs.json",
    "LOG": "DEBUG",
    "DATE_FROM": "2025/01",
    "DATE_TO": "2025/02",
    "SSL_CHECK": "True"
}

[INFO]  Retrieve metadata of running SLAs in progress...

[DEBUG] Fetching the active *SLAs* in progress...
	This operation may take few minutes to complete. Please wait!

[INFO] The accounting_period *ALREADY FOUND* in the gspread at row: 38 

[DEBUG] Downloading accounting records from the EGI Accouting Portal in progress...
	This operation may take few minutes to complete. Please wait!

[INFO]  Fetching the accounting records for the VO [BIOMED] in progress...
https://accounting.egi.eu/egi/elap_processors/REGION/Year/2025/01/2025/02/custom-biomed/onlyinfrajobs/JSON/ [{'2025': 36943.617, 'id': 'NGI_FRANCE', 'Total': 36944, 'Percent': 49.64}, {'2025': 400.9181, 'id': 'NGI_IBERGRID', 'Total': 401, 'Percent': 0.54}, {'2025': 52.1512, 'id': 'NGI_TR', 'Total': 52, 'Percent': 0.07}, {'2025': 31101.8829, 'id': 'NGI_UK', 'Total': 31102, 'Percent': 41.79}, {'2025': 5932.3062, 'id': 'Russia', 'Total': 5932, 'Percent': 7.97}, {'2025': 74431, 'id': 'Total', 'Total': 74431, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_FRANCE', '1': 'NGI_IBERGRID', '2': 'NGI_TR', '3': 'NGI_UK', '4': 'Russia'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'elap_processors'}]
- Resource Centre: NGI_FRANCE; CPU/h:  36,944
- Resource Centre: NGI_IBERGRID; CPU/h:     401
- Resource Centre: NGI_TR; CPU/h:      52
- Resource Centre: NGI_UK; CPU/h:  31,102
- Resource Centre: Russia; CPU/h:   5,932
- Total HTC CPU/h =  74,431
[INFO] The vo 'biomed' is *already* in the gspread at position: 2
[INFO] Updated the total HTC CPU/h for the VO

[INFO]  Fetching the accounting records for the VO [ENMR.EU] in progress...
https://accounting.egi.eu/egi/elap_processors/REGION/Year/2025/01/2025/02/custom-enmr.eu/onlyinfrajobs/JSON/ [{'2025': 217164.8079, 'id': 'NGI_DE', 'Total': 217165, 'Percent': 10.85}, {'2025': 29692.742, 'id': 'NGI_IT', 'Total': 29693, 'Percent': 1.48}, {'2025': 1366946.3057, 'id': 'NGI_NL', 'Total': 1366946, 'Percent': 68.31}, {'2025': 387190.0013, 'id': 'NGI_UK', 'Total': 387190, 'Percent': 19.35}, {'2025': 2000994, 'id': 'Total', 'Total': 2000994, 'Percent': ''}, {'2025': '100.00%', 'id': 'Percent', 'Percent': '', 'Total': ''}, {'id': 'xlegend', '0': 'NGI_DE', '1': 'NGI_IT', '2': 'NGI_NL', '3': 'NGI_UK'}, {'id': 'ylegend', '0': 2025, '1': 'id'}, {'id': 'var', 'xrange': 'Year', 'yrange': 'REGION', 'query': 'elap_processors'}]
- Resource Centre: NGI_DE; CPU/h: 217,165
- Resource Centre: NGI_IT; CPU/h:  29,693
- Resource Centre: NGI_NL; CPU/h: 1,366,946
- Resource Centre: NGI_UK; CPU/h: 387,190
- Total HTC CPU/h = 2,000,994
[INFO] The vo 'enmr.eu' is *already* in the gspread at position: 3
[INFO] Updated the total HTC CPU/h for the VO

[REPORT]
- HTC CPU/h consumed by the EGI SLAs
- Reporting period = 2025/01 - 2025/02
- Total = 2,075,425 HTC CPU/h
[INFO] Updated the total HTC CPU/h for the VO
```

The VO statistics are updated in the Google worksheet `Accounting SLAs HTC CPU/h`

