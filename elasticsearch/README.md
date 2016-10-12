elastictasks
============

Small script to handle some recurrent tasks related to Elasticsearch.

**Note**: tasks like opening or closing indices based on X days (older than X) are expecting to find an index name format like logstash-YYYY.MM.DD

TODOS: Snapshots and related task like setting a repository, range for days in open/close indices.

First you need to install elasticsearch.py

```bash
pip install elasticsearch
```

Usage
```
$ ./elastictask.py -h
usage: elastictask.py [-h] -s SERVER [-p PORT] [-c | -o | -l]
                      [-i INDEX [INDEX ...] | -d DAYS]

Script to handle some common tasks in Elasticsearch

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Elasticsearch Address
  -p PORT, --port PORT  Elasticsearch Port
  -c, --close           List Closed Indices or Action to Close when used with
                        -d or -i
  -o, --open            List Open Indices or Action to Open when used with
                        -d or -i
  -l, --list            List all indices
  -i INDEX [INDEX ...], --index INDEX [INDEX ...]
                        Indices List
  -d DAYS, --days DAYS  Age in days, older than this will be open or close.
```

List all indices.

```
$ ./elastictask.py -s elk.aldoca.local -l
Server: elk.aldoca.local
Port: 9200

Indices: 17
======================================================================
close logstash-2016.09.11
close logstash-2016.09.13
close logstash-2016.09.14
close logstash-2016.09.15
yellow open .kibana 1 1 140 1 123.5kb 123.5kb
yellow open logstash-2016.09.16 5 1 742 0 691.5kb 691.5kb
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
yellow open logstash-2016.10.12 5 1 226 0 455.5kb 455.5kb
```

List closed indices.

```
$ ./elastictask.py -s elk.aldoca.local -c
Server: elk.aldoca.local
Port: 9200

Close Indices: 4
======================================================================
close logstash-2016.09.11
close logstash-2016.09.13
close logstash-2016.09.14
close logstash-2016.09.15
```

List open indices.
```
$ ./elastictask.py -s elk.aldoca.local -o
Server: elk.aldoca.local
Port: 9200

Open Indices: 13
======================================================================
yellow open .kibana 1 1 140 1 123.5kb 123.5kb
yellow open logstash-2016.09.16 5 1 742 0 691.5kb 691.5kb
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
yellow open logstash-2016.10.12 5 1 228 0 475.5kb 475.5kb
```

When you combine option "--close" or "--open" with "--days" or "--index" you can open or close the indices according to the specified in the last argument.

**Note**: When opening or closing indices, kibana index is ignored.

Closing indices older than 10 days.

```
]$ ./elastictask.py -s elk.aldoca.local -c -d 10
Server: elk.aldoca.local
Port: 9200

Closing:
logstash-2016.09.16
logstash-2016.09.17
logstash-2016.09.18
logstash-2016.09.19
logstash-2016.09.20
logstash-2016.09.21
logstash-2016.09.22
logstash-2016.09.23
logstash-2016.09.30
```

Open just a couple of indices.
```
$ ./elastictask.py -s elk.aldoca.local -o -i logstash-2016.09.30 logstash-2016.09.23
Server: elk.aldoca.local
Port: 9200

Opening:
logstash-2016.09.30
logstash-2016.09.23
```
