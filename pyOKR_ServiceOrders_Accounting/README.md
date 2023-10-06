# pyOKR_ServiceOrders_Accounting

This python client calculates the number of Service Orders received from the [EOSC Marketplace](https://marketplace.eosc-portal.eu/).

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

## Calculate the Service Orders received in the specific period

This python client calculates the number of Service Orders received from the [EOSC MarketPlace](https://marketplace.eosc-portal.eu/).

## Edit the environmental settings

Edit the `openrc.sh` file and configure the settings.

```bash
# EGI Jira portal settings
export JIRA_SERVER_URL="https://jira.egi.eu/"
export JIRA_AUTH_TOKEN="MTMzNDkxMjYwNzg2OlGxzek1UQ0qIV0pa0c8yXk9BvAI"

# Project used for the Customers' complains
export COMPLAINS_PROJECTKEY="EGIREQ"

# Project used for the VO SLA violations
export VIOLATIONS_PROJECTKEY="IMSSLA"
export ISSUETYPE="SLA Violation"

# Project used for the Service Orders
export SERVICE_ORDERS_PROJECTKEY="EOSCSO"
#export SERVICE_ORDERS_ISSUETYPE="Epic"
export SERVICE_ORDERS_ISSUETYPE="Service order"

# Google Spreadsheet settings
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_SERVICE_ORDERS_WORKSHEET="Service Orders"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
export LOG="INFO"
#export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"

export DATE_FROM="2020/01"
export DATE_TO="2020/03
```

## Calculate the number of Service Orders received (in the specific period)

```bash
$ source openrc.sh && python3 pyOKR_ServiceOrders_Accounting_v0.4.py

Log Level = INFO

Generating reporting in progress...
This operation may take a few minutes to complete. Please wait!

[INFO] Reporting Period = 2020.01-03
The header '2020.01-03' is *already* in the Worksheet

[INFO]  Updating the Service Orders of the EGI services *already existing* in the worksheet in progress..
	This operation may take few minutes. Please wait!

Updated the #SOs [1] for the service: EGI Check-In
Updated the #SOs [4] for the service: EGI Cloud Compute
Updated the #SOs [0] for the service: EGI Cloud Container Compute
Updated the #SOs [0] for the service: EGI DataHub
[WARNING] Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'
Updated the #SOs [0] for the service: EGI Data Transfer
Updated the #SOs [0] for the service: EGI FitSM Training
[WARNING] Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'
Updated the #SOs [0] for the service: EGI Infrastructure Manager
Updated the #SOs [5] for the service: EGI Notebooks
Updated the #SOs [1] for the service: EGI Online Storage
Updated the #SOs [0] for the service: EGI Replay
Updated the #SOs [1] for the service: EGI ISO 27001 Training
Updated the #SOs [0] for the service: EGI Software Distribution
Updated the #SOs [0] for the service: EGI Training Infrastructure
Updated the #SOs [0] for the service: EGI Workload Manager
[INFO]  Service Orders updated in the Google worksheet!
```

The Service Orders statistics are updated in the Google worksheet `Service Orders`
