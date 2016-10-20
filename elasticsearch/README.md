elastictasks
============

Small script to handle some recurrent tasks related to Elasticsearch.

**Note**: tasks like opening or closing indices based on X days (older than X) are expecting to find an index name format like logstash-YYYY.MM.DD

First you need to install elasticsearch.py

```bash
pip install elasticsearch
```

Usage
```
$ ./elastictask.py -h
usage: elastictask.py [-h] -s SERVER [-p PORT]
                      {indices,snapshot,repository} ...

Script to handle some common tasks in Elasticsearch

positional arguments:
  {indices,snapshot,repository}
                        commands
    indices             Actions with indices
    snapshot            Actions with snapshots
    repository          Actions with repositories

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Elasticsearch Address
  -p PORT, --port PORT  Elasticsearch Port
```

You can check the help for the different arguments (indices, snapshot, repo).

```
$ ./elastictask.py indices -h
usage: elastictask.py indices [-h] [-l | -o | -c] [-i INDEX [INDEX ...] | -d
                              DAYS]

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List all indices
  -o, --open            List open indices
  -c, --close           List closed indices
  -i INDEX [INDEX ...], --index INDEX [INDEX ...]
                        Indices List
  -d DAYS, --days DAYS  Age in days, older than this will be open or close
```

List all indices.

```
$ ./elastictask.py -s elk.aldoca.local indices --list
Indices: 18
======================================================================
close logstash-2016.09.11
close logstash-2016.09.13
close logstash-2016.09.14
close logstash-2016.09.15
close logstash-2016.09.16
red open logstash-2016.10.13 5 1 54 0 291.7kb 291.7kb
yellow open .kibana 1 1 140 1 123.5kb 123.5kb
yellow open logstash-2016.09.17 5 1 913 0 753kb 753kb
yellow open logstash-2016.09.18 5 1 697 0 360.8kb 360.8kb
yellow open logstash-2016.09.19 5 1 1210 0 857.8kb 857.8kb
yellow open logstash-2016.09.20 5 1 2808 0 966kb 966kb
yellow open logstash-2016.09.21 5 1 1326 0 1mb 1mb
yellow open logstash-2016.09.22 5 1 536 0 290.8kb 290.8kb
yellow open logstash-2016.09.23 5 1 1543 0 469.3kb 469.3kb
yellow open logstash-2016.09.30 5 1 60 0 218.4kb 218.4kb
yellow open logstash-2016.10.01 5 1 54 0 267.2kb 267.2kb
yellow open logstash-2016.10.11 5 1 96 0 256.5kb 256.5kb
yellow open logstash-2016.10.12 5 1 354 0 296.1kb 296.1kb
```

List closed indices.

```
$ ./elastictask.py -s elk.aldoca.local indices --close
Close Indices: 5
======================================================================
close logstash-2016.09.11
close logstash-2016.09.13
close logstash-2016.09.14
close logstash-2016.09.15
close logstash-2016.09.16
```

List open indices.

```
$ ./elastictask.py -s elk.aldoca.local indices --open
Open Indices: 13
======================================================================
red open logstash-2016.10.13 5 1 59 0 357.4kb 357.4kb
yellow open .kibana 1 1 140 1 123.5kb 123.5kb
yellow open logstash-2016.09.17 5 1 913 0 753kb 753kb
yellow open logstash-2016.09.18 5 1 697 0 360.8kb 360.8kb
yellow open logstash-2016.09.19 5 1 1210 0 857.8kb 857.8kb
yellow open logstash-2016.09.20 5 1 2808 0 966kb 966kb
yellow open logstash-2016.09.21 5 1 1326 0 1mb 1mb
yellow open logstash-2016.09.22 5 1 536 0 290.8kb 290.8kb
yellow open logstash-2016.09.23 5 1 1543 0 469.3kb 469.3kb
yellow open logstash-2016.09.30 5 1 60 0 218.4kb 218.4kb
yellow open logstash-2016.10.01 5 1 54 0 267.2kb 267.2kb
yellow open logstash-2016.10.11 5 1 96 0 256.5kb 256.5kb
yellow open logstash-2016.10.12 5 1 354 0 296.1kb 296.1kb
```

When you combine option "--close" or "--open" with "--days" or "--index" you can open or close the indices according to the specified in the last argument.

**Note**: When opening or closing indices, kibana index is ignored in the script.

Closing indices older than 10 days.

```
$ ./elastictask.py -s elk.aldoca.local indices -c -d 10
Closing:
logstash-2016.09.17
logstash-2016.09.18
logstash-2016.09.19
logstash-2016.09.20
logstash-2016.09.21
logstash-2016.09.22
logstash-2016.09.23
logstash-2016.09.30
logstash-2016.10.01
```

Open just a couple of indices.

```
$ ./elastictask.py -s elk.aldoca.local indices --open --index logstash-2016.10.01 logstash-2016.09.30
Opening:
logstash-2016.10.01
logstash-2016.09.30
```

List Repositories.

```
$ ./elastictask.py -s elk.aldoca.local repo --list
{
    "archives": {
        "type": "fs",
        "settings": {
            "compress": "true",
            "location": "/backups/archives"
        }
    }
}
```

Show Snapshots in the 'archives' repository.

```
$ ./elastictask.py -s elk.aldoca.local snapshot --repo archives --list
{
    "snapshots": [
        {
            "duration_in_millis": 7423,
            "start_time": "2016-09-22T00:45:20.687Z",
            "shards": {
                "successful": 10,
                "failed": 0,
                "total": 10
            },
            "version_id": 2040099,
            "end_time_in_millis": 1474505128110,
            "state": "SUCCESS",
            "version": "2.4.0",
            "snapshot": "snapshot_1",
            "end_time": "2016-09-22T00:45:28.110Z",
            "indices": [
                "logstash-2016.09.11",
                "logstash-2016.09.13"
            ],
            "failures": [],
            "start_time_in_millis": 1474505120687
        }
    ]
}
```

Creating snapshot 'snapshot_2' in 'archives' repository.

```
$ ./elastictask.py -s elk.aldoca.local snapshot --repo archives --create snapshot_2 --index logstash-2016.09.22 logstash-2016.09.23
Creating Snapshot for:
['logstash-2016.09.22,logstash-2016.09.23']
```

Deleting snapshot 'snapshot_1' in 'archives' repository.

```
$ ./elastictask.py -s elk.aldoca.local snapshot --repo archives --delete snapshot_1
Deleting snapshots: snapshot_1 in repository: archives
```
