zfssainfo.py
============

Client to get some info from ZFS Storage Appliance using REST api service.

LUN output:
```
==========================================================================================================================================================================
LUN             Size(GB) TargetGroup     InitiatorGroup       status     lunguid                            Pool     Project                   logbias  assignednumber
==========================================================================================================================================================================
VSO00            1024.00 default         ['NODE000-009']     online     600144F0F2XXXXXXXXXXXXXXXXXXX001   pool_0   VMWPRD000                  latency     0
VSO01            1024.00 default         ['NODE000-009']     online     600144F0F2XXXXXXXXXXXXXXXXXXX002   pool_0   VMWPRD000                  latency     1
VSO02             200.00 default         ['NODE000-009']     online     600144F0E6XXXXXXXXXXXXXXXXXXX06E   pool_0   VMWPRD000                  latency     2
```

FILESYSTEM output:
```
======================================================================================================================================================================================================================================
FSNAME               space(GB) mountpoint                               pool     project                quota    reserv   root_user  root_group perm  sharesmb                                 sharenfs                                          
======================================================================================================================================================================================================================================
share000                76.29 /export/share_priv/share000              pool_2   share_priv               100.00     0.00 nobody     other      700   off                                      sec=sys,rw,root=@192.168.100.0/24                    
redotemp01              25.00 /export/share_public/redotemp01          pool_2   share_public              25.00    25.00 1000       1001       775   off                                      sec=sys,rw,root=@192.168.100.0/24                     
img                    100.00 /export/share_public/img                 pool_2   share_public             100.00   100.00 1032       1001       775   on,abe=off,dfsroot=false                 sec=sys,rw,root=@192.168.100.0/24:@192.168.200.0/24    
appX_img                15.00 /export/share_public/appX_img            pool_2   share_public              15.00    15.00 nobody     other      775   name=bduc_img,abe=off,dfsroot=false      sec=sys,rw,root=@192.168.100.0/24:@192.168.200.10/24:@192.168.200.20/24
installers               5.00 /export/Windows/installers               pool_2   Windows                    5.00     5.00 nobody     other      755   on,abe=off,dfsroot=false                
```