
## Calculate the Cloud CPU/h consumed in the specific period

Edit the `openrc.sh` file and configure the `scope=cloud`

```
[..]
export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
export ACCOUNTING_SCOPE="cloud" # for Cloud Compute

# Available metrics (for scope=cloud): 
# 'sum_elap_processors', 'mem-GByte', 'vm_num', 'sum_elap', 'cost', 'net_in', 'net_out', 'disk', 'processors'
export ACCOUNTING_METRIC="sum_elap_processors"

export DATE_FROM="2023/01"
export DATE_TO="2023/06"
```

Source the environment settings and run the client

```
]$ source openrc.sh && python3 pyVOs_CPUs_Accounting_v0.2.py 

Log Level = INFO

[INFO]     Reporting Period: 2020.01-06
[Cloud]    Total Cloud CPU/h = 12,050,254
[noVOCPUs] VOs with *no* accounting records (3)
[VOCPUs]   VOs with *accounting* records (47)
```

## Calculate the HTC CPU/h consumed in the specific period

Edit the `openrc.sh` file and configure the `scope=egi`

```
[..]
export ACCOUNTING_SERVER_URL="https://accounting.egi.eu"

# Available scope: 'cloud', 'egi'
export ACCOUNTING_SCOPE="egi" # for HTC Compute

# Available metrics (for scope=grid):
# 'elap_processors', 'njobs', 'normcpu', 'sumcpu', 'normelap', 'normelap_processors', 'sumelap', 'cpueff'
export ACCOUNTING_METRIC="elap_processors"

export DATE_FROM="2023/01"
export DATE_TO="2023/06"
```

```
]$ source openrc.sh && python3 pyVOs_CPUs_Accounting_v0.2.py 

Log Level = INFO

[INFO]     Reporting Period: 2020.01-06
[HTC]      Total HTC CPU/h = 2,677,303,881
[noVOCPUs] VOs with *no* accounting records (3)
[VOCPUs]   VOs with *accounting* records (60)
```

