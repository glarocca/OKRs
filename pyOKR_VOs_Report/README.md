# pyOKR_VOs_Report

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

## Generate a VOs report in the specific period

This python client generates a report of the VOs that are in following status:

* Production (P),
* Leaving (L),
* Deleted (D), or
* Pending (PE)

## Edit the environment settings

```bash
#  EGI Operations Portal serttings
export OPERATIONS_SERVER_URL="https://operations-portal.egi.eu/api/"
export OPERATIONS_API_KEY="******************"
export OPERATIONS_FORMAT="json"
export OPERATIONS_VOS_REPORT_PREFIX="egi-reports"

# Google Spreadsheet settings
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_VOS_REPORT_WORKSHEET="Num. of VOs created"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"

export DATE_FROM="2020/01"
export DATE_TO="2020/03"
```

Source the environment settings and run the client

```bash
]$ source openrc.sh && python3 pyVOs_VOs_Report_v0.1.py

Log Level = DEBUG

- Environment settings:
{
    "OPERATIONS_SERVER_URL": "https://operations-portal.egi.eu/api/",
    "OPERATIONS_API_KEY": "*******************",
    "OPERATIONS_FORMAT": "json",
    "OPERATIONS_VOS_REPORT_PREFIX": "egi-reports",
    "SERVICE_ACCOUNT_PATH": "/home/larocca/test/OKRs/pyOKR_VOs_Report/.config/",
    "SERVICE_ACCOUNT_FILE": "/home/larocca/test/OKRs/pyOKR_VOs_Report/.config/service_account.json",
    "GOOGLE_SHEET_NAME": "OKR_Reports",
    "GOOGLE_VOS_REPORT_WORKSHEET": "Num. of VOs created",
    "LOG": "DEBUG",
    "DATE_FROM": "2022/07",
    "DATE_TO": "2022/09",
    "SSL_CHECK": "True"
}

[INFO]  Reporting Period: 2022.07-09

[LOG]   List of VOs creation and deletion during the reporting period
[
    {
        "status": "Leaving",
        "count": "1",
        "vos": [
            "vo.fuvex.es(L)"
        ]
    },
    {
        "status": "Production",
        "count": "3",
        "vos": [
            "eval.c-scale.eu(P)",
            "vo.qc-md.eli-np.eu(P)",
            "vo.fuvex.es(P)"
        ]
    }
]
[INFO]  Updated the VOs reports for the reporting period: 2022.07-09
```

The VO statistics are updated in the Google worksheet `Num. of VOs created`
