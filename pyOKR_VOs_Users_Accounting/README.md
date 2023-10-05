# pyOKR_VOs_Users_Accounting

This python client calculates the number of users of the production VOs.

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
export GOOGLE_VOS_WORKSHEET="VOs statistics"

export DATE_FROM="2023/01"
export DATE_TO="2023/06"
```

## Calculate the number of users of the production VOs (in the specific period)

```
]$ source openrc.sh && python3 pyVOs_Users_Accounting_v0.5.py 2>&1 out

Log Level = INFO

[INFO] 	Reporting Period: '2021.07-12'
	The header '2021.07-12' is *already* in the Worksheet

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
