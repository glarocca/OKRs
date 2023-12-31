# pyOKR_VOs_Users_Accounting

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

## Calculate the Service Orders received in the specific period

This python client calculates the number of users of the production VOs registered in the [EGI Operations Portal](https://operations-portal.egi.eu/).

## Edit the environmental settings

Edit the `openrc.sh` file and configure the settings.

```
[..]
# EGI Operations Portal settings
export OPERATIONS_SERVER_URL="https://operations-portal.egi.eu/api/"
export OPERATIONS_API_KEY="***********"
export OPERATIONS_FORMAT="json"
export OPERATIONS_VO_LIST_PREFIX="vo-list"
export OPERATIONS_VO_ID_CARD_PREFIX="vo-idcard"
export OPERATIONS_VOS_REPORT_PREFIX="egi-reports"

# Google Spreadsheet settings
export SERVICE_ACCOUNT_PATH=${PWD}"/.config/"
export SERVICE_ACCOUNT_FILE=${SERVICE_ACCOUNT_PATH}"service_account.json"
export GOOGLE_SHEET_NAME="OKR_Reports"
export GOOGLE_VOS_WORKSHEET="VOs statistics (certs)"

# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# SSL_CHECK=False, SSL check is disabled
export SSL_CHECK="True"
#export SSL_CHECK="False"

export DATE_FROM="2021/01"
export DATE_TO="2021/03"
```

## Calculate the number of users of the production VOs (in the specific period)

```
]$ source openrc.sh && python3 pyVOs_Users_Accounting_v0.5.py

Log Level = INFO

[INFO] 	Reporting Period: '2021.01-03'
	The header '2021.01-03' is *already* in the Worksheet

[INFO] 	Downloading the VOs metadata from the EGI Operations Portal in progress..
	This operation may take few minutes. Please wait!

0.) Fetching metadata for the VO [aegis] in progress..
1.) Fetching metadata for the VO [alice] in progress..
2.) Fetching metadata for the VO [ams02.cern.ch] in progress..
3.) Fetching metadata for the VO [apesci] in progress..
4.) Fetching metadata for the VO [argo] in progress..
[..]
304.) Fetching metadata for the VO [vo.latitudo40.com.eu] in progress..
305.) Fetching metadata for the VO [vo.bioexcel.eu] in progress..
306.) Fetching metadata for the VO [vo.tools.egi.eu] in progress..
307.) Fetching metadata for the VO [vo.openbiomaps.org] in progress..
308.) Fetching metadata for the VO [vo.waltoninstitute.ie] in progress..

[INFO] 	Updating statistics of the VOs *already existing* in the Google worksheet in progress..
	This operation may take few minutes. Please wait!
Updated statistics for the VO [EOServices-vo.indra.es]
Updated statistics for the VO [ams02.cern.ch]
Updated statistics for the VO [HighResLandSurf.c-scale.eu]
Updated statistics for the VO [afigrid.cl]
[WARNING] Quota exceeded for metric 'Write requests' and 'Write requests per minute per user'
Updated statistics for the VO [cryoem.instruct-eric.eu]
Updated statistics for the VO [culturalheritage.vo.egi.eu]
Updated statistics for the VO [d4science.org]
Updated statistics for the VO [dech]
Updated statistics for the VO [deep-hybrid-datacloud.eu]
Updated statistics for the VO [demo.fedcloud.egi.eu]
Updated statistics for the VO [desy]
Updated statistics for the VO [desy-cc.de]
[..]
Updated statistics for the VO [vo.waltoninstitute.ie]
Updated statistics for the VO [waterwatch.c-scale.eu]
Updated statistics for the VO [worsica.vo.incd.pt]
Updated statistics for the VO [xenon.biggrid.nl]
Updated statistics for the VO [xfel.eu]
Updated statistics for the VO [zeus]
[INFO]  Existing VOs statistics updated in the Google worksheet!

[INFO] 	Insert *new VOs* and related statistics in the Google worksheet in progress..
	This operation may take few minutes. Please wait!
[INFO]  [0] *new* VO statistics added in the Google worksheet!
```

The VO statistics are updated in the Google worksheet `VOs statistics`
