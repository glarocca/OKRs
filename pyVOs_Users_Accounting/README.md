This python client shows the number of VO users in the specific reporting period.

## Edit the environmental settings
Edit the `openrc.sh` file and configure the settings
```
[..]
# EGI Operations Portal settings
export OPERATIONS_SERVER_URL="https://operations-portal.egi.eu/api/"
export OPERATIONS_API_KEY="***********"
export OPERATIONS_FORMAT="json"
export OPERATIONS_VO_LIST_PREFIX="vo-list"
export OPERATIONS_VO_ID_CARD_PREFIX="vo-idcard"
export OPERATIONS_VOS_REPORT_PREFIX="egi-reports"

export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_VOS_WORKSHEET="VOs statistics"

export DATE_FROM="2023/01"
export DATE_TO="2023/06"
```
