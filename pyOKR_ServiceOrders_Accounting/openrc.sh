#!/bin/bash

#######################################################
# E G I ** J I R A ** P O R T A L **  S E T T I N G S #
#######################################################
export JIRA_SERVER_URL="https://jira.egi.eu/"
export JIRA_AUTH_TOKEN="<ADD_JIRA_AUTH_TOKEN>"

# Project used for the Customers' complains
export COMPLAINS_PROJECTKEY="EGIREQ"

# Project used for the Service Orders
export SERVICE_ORDERS_PROJECTKEY="EOSCSO"
#export SERVICE_ORDERS_ISSUETYPE="Epic"
export SERVICE_ORDERS_ISSUETYPE="Service order"

###########################################################
# G O O G L E ** S P R E A D S H E E T ** S E T T I N G S #
###########################################################
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
export DATE_TO="2020/03"
