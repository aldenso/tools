auditlogs
=========

Small python script to check if some directories have more logs than is healthy, based on values you'll set for logs size and count.

Set your values:
```python
# Size 10 MB
SIZEALERT = 10 * (1024 * 1024)
COUNTALERT = 100
DATETIME = datetime.now().strftime("%d%m%y_%H%M%S")

DIRS = [
    ["/export/home", 10 * 1024 * 1024, 100],
    ["/var", 10485760, 100],
    ["/root"]
]
EXT = [".log", ".xml", ".aud"]
```

Every directory list inside DIRS needs to be 1 or 3 in length, if its 1 for that directory, it will use the defaults (SIZEALERT and COUNTALERT).


Output sample:
```
# python auditlogs.py
###############################################################################
logs for /export/home:
Count: 0
Full size: 0MB
###############################################################################
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@********** WARNING ********** WARNING ********** WARNING **********@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
CHECK LOG SIZE UTILIZATIONs
Alertsize: 10MB || Alertcount: 100
directory: /var
size: 101MB || count: 207
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@********** WARNING ********** WARNING ********** WARNING **********@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Logs distribution:
Dir: /var/fm/fmd/topo/ddae174f-e813-6c2d-b981-8c6e94e13e31 || size: 43845 || Count:  1
Dir: /var/fm/fmd/topo/9b856161-e1b5-6e3c-8842-c3b406acd115 || size: 43845 || Count:  1
Dir: /var/ocm/ccr/config/default || size:  0 || Count:  1
Dir: /var/svc/log || size: 1441067 || Count: 170
Dir: /var/ocm/ccr/log || size:  0 || Count:  3
Dir: /var/ai/profile || size: 6523 || Count:  1
Dir: /var/tmp/manifests || size: 9900 || Count:  3
Dir: /var/log || size: 104857600 || Count:  1
Dir: /var/pkg/history || size: 107606 || Count: 19
Dir: /var/log/ilomconfig || size: 9798 || Count:  1
Dir: /var/fm/fmd/topo/63db6cea-e859-4237-a245-acdeb72e1607 || size: 43845 || Count:  1
Dir: /var/log/pkg/sysrepo || size:  0 || Count:  1
Dir: /var/fm/fmd/topo/8cf65114-562c-cb8d-e2b7-f54277c7e307 || size: 43845 || Count:  1
Dir: /var/sadm/servicetag/registry || size: 872 || Count:  1
Dir: /var/svc/manifest/site || size: 641 || Count:  1
Dir: /var/fm/fmd/topo/407a6abf-a31e-6275-af5d-bd10d1db1d59 || size: 43845 || Count:  1
*******************************************************************************

# ls -lrth warning*
-rw-r--r--   1 root     root         658 Jun 26 20:41 warning_var_260616_204057.log

# head -5 warning_var_260616_204057.log
directory,size in bytes,number of logs
/var/fm/fmd/topo/ddae174f-e813-6c2d-b981-8c6e94e13e31,43845,1
/var/fm/fmd/topo/9b856161-e1b5-6e3c-8842-c3b406acd115,43845,1
/var/ocm/ccr/config/default,0,1
/var/svc/log,1441067,170
```
