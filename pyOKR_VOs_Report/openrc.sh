#!/bin/bash

##################################################################
# E G I ** O P E R A T I O N S ** P O R T A L ** S E T T I N G S #
##################################################################
export OPERATIONS_SERVER_URL="https://operations-portal.egi.eu/api/"
export OPERATIONS_API_KEY="61ba1a4deec9c"
export OPERATIONS_FORMAT="json"
export OPERATIONS_VOS_REPORT_PREFIX="egi-reports"

export DATE_FROM="2022/07"
export DATE_TO="2022/09"

###########################################################
# G O O G L E ** S P R E A D S H E E T ** S E T T I N G S #
###########################################################
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
