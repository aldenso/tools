#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-10-11T21:17:52-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-10-12T21:33:02-04:00

from elasticsearch import Elasticsearch
from datetime import datetime
from collections import namedtuple
import json
import socket
import sys
import argparse


class Info:
    """
    General info from elasticsearch.
    """

    def __init__(self, esinst):
        self.esinst = esinst
        self.idxs = self.getIndices().list

    def getInfo(self):
        info = self.esinst.info()
        return json.dumps(info, indent=4)

    def getIndices(self):
        indices = self.esinst.cat.indices()
        idxs = sorted([" ".join(x.strip().split())
                      for x in indices.split("\n")])
        idxs.remove('')
        Indices = namedtuple("Indices", "list listinlines count")
        return Indices(list=idxs, listinlines="\n".join(idxs),
                       count=len(idxs))

    def getIndicesOpen(self):
        """Returns open indices as list, as multiline list and list length"""
        openidxs = [x for x in self.idxs if "open" in x]
        OpenIndices = namedtuple("OpenIndices", "list listinlines count")
        return OpenIndices(list=openidxs, listinlines="\n".join(openidxs),
                           count=len(openidxs))

    def getIndicesClose(self):
        """Returns close indices as list, as multiline list and list length"""
        closeidxs = [x for x in self.idxs if "close" in x]
        CloseIndices = namedtuple("CloseIndices", "list listinlines count")
        return CloseIndices(list=closeidxs, listinlines='\n'.join(closeidxs),
                            count=len(closeidxs))

    def getHealth(self):
        health = self.esinst.cat.health()
        header = "epoch timestamp cluster status node.total node.data "
        "shards pri relo init unassign\n"
        return "{}{}".format(header, health)

    def getNodes(self):
        nodes = self.esinst.cat.nodes()
        header = "nodes ip heap.percent ram.percent load node.role master "
        "name\n"
        return "{}{}".format(header, nodes)

    def getDocsCount(self):
        count = self.esinst.cat.count()
        return count.split(" ")[2]

    def getIndicesToOpen(self, days):
        data = self.getIndicesClose()[1]
        toopen = []
        datalist = data.split("\n")
        for x in datalist:
            # Avoid read kibana index
            if "kibana" in x:
                continue
            # health status index pri rep docs.count docs.deleted store.size
            # pri.store.size
            [status, index] = x.split(" ")
            datestamp = "".join(index.split("-")[-1:])
            index_date = datetime.strptime(str(datestamp), "%Y.%m.%d")
            diff = datetime.now() - index_date
            if diff.days > days:
                toopen.append(index)
        return toopen

    def getIndicesToClose(self, days):
        data = self.getIndicesOpen()[1]
        toclose = []
        datalist = data.split("\n")
        for x in datalist:
            # Avoid read kibana index
            if "kibana" in x:
                continue
            # health status index pri rep docs.count docs.deleted store.size
            # pri.store.size
            [health, status, index, pri, rep,
                docs_count, docs_deleted, store_size,
                pri_store_size] = x.split(" ")
            datestamp = "".join(index.split("-")[-1:])
            index_date = datetime.strptime(str(datestamp), "%Y.%m.%d")
            diff = datetime.now() - index_date
            if diff.days > days:
                toclose.append(index)
        return toclose


class Modify:
    """
    Modify elasticsearch indices provided as a list (example: a list returned
    from Info.getIndicesToClose).
    """

    def __init__(self, esinst, idxlist):
        self.esinst = esinst
        self.idxlist = idxlist

    def Exists(self):
        """Check if the indices list exists."""
        try:
            exists = self.esinst.indices.exists(index=self.idxlist)
        except Exception as err:
            print("Error: {}".format(err))
        else:
            if not exists:
                print("Indices not found")
                sys.exit(1)

    def Close(self):
        """Close indices in the args list."""
        self.Exists()
        for idx in self.idxlist:
            try:
                self.esinst.indices.close(index=idx)
            except Exception as err:
                print("Error: {}".format(err))

    def Open(self):
        """Open indices in the args list."""
        self.Exists()
        for idx in self.idxlist:
            try:
                self.esinst.indices.open(index=idx)
            except Exception as err:
                print("Error: {}".format(err))


class Snapshot:
    """
    Work with elasticsearch snapshots.
    """

    def __init__(self, esinst, repo, **kwargs):
        self.esinst = esinst
        self.repo = repo
        self.snapname = kwargs.get("snapname", None)
        self.idxlist = kwargs.get("idxlist", None)

    def showSnap(self):
        show = self.esinst.snapshot.get(
            repository=self.repo, snapshot="_all")
        return json.dumps(show, indent=4)

    def createSnap(self):
        pass


class Repository:
    """
    Work with elasticsearch repositories.
    """

    def __init__(self, esinst, repo):
        self.esinst = esinst
        self.repo = repo

    def listRepo(self):
        if self.repo is not None:
            list = self.esinst.snapshot.get_repository(
                repository="_all")
            return json.dumps(list, indent=4)
        else:
            list = self.esinst.snapshot.get_repository(
                repository=self.repo)
            return json.dumps(list, indent=4)


def is_reachable(SERVER, PORT):
    """Check if the server and port is reachable."""
    try:
        s = socket.create_connection((SERVER, PORT), None)
        s.close()
        return True
    except Exception as err:
        print("Error: {}".format(err))
        sys.exit(1)


def get_args():
    """Get arguments passed in"""
    parser = argparse.ArgumentParser(
        description="Script to handle some common tasks in Elasticsearch")
    parser.add_argument(
        "-s", "--server", type=str,
        help="Elasticsearch Address",
        required=True)
    parser.add_argument(
        "-p", "--port", type=int,
        help="Elasticsearch port",
        default=9200,
        required=False)
    subparserrepo = parser.add_subparsers(help="commands", dest="parser_name")
    # Parser for Indices
    indices = subparserrepo.add_parser("indices", help="Actions with indices")
    idxgroup1 = indices.add_mutually_exclusive_group()
    idxgroup1.add_argument("-l", "--list", help="List all indices",
                           action="store_true")
    idxgroup1.add_argument("-o", "--open", help="List open indices",
                           action="store_true")
    idxgroup1.add_argument("-c", "--close", help="List closed indices",
                           action="store_true")
    idxgroup2 = indices.add_mutually_exclusive_group()
    idxgroup2.add_argument("-i", "--index", type=str, help="Indices List",
                           nargs="+")
    idxgroup2.add_argument(
        "-d", "--days", type=int,
        help="Age in days, older than this will be open or close")
    # Parser for snapshots
    snap = subparserrepo.add_parser("snapshot", help="Actions with snapshots")
    snap.add_argument("-l", "--list", action="store_true",
                      help="Show Snapshot in specified repo")
    snap.add_argument("--repo", action="store", help="Repository to use",
                      required=True)
    snapgroup1 = snap.add_mutually_exclusive_group()
    snapgroup1.add_argument("--create", action="store", help="Create Snapshot")
    snapgroup1.add_argument("--delete", action="store", help="Delete Snapshot")
    # Parser for repositories
    repo = subparserrepo.add_parser("repo", help="Actions with repositories")
    repo.add_argument("-l", "--list", action="store_true")
    repo.add_argument("--repo", action="store")

    args = parser.parse_args()
    return args


def indicesCommands(es, info, args):
    INDICES = args.list
    OPEN = args.open
    CLOSE = args.close
    INDEX = args.index
    DAYS = args.days
    if INDICES:
        indicesinfo = info.getIndices()
        print("Indices: {}\n{}\n{}\n"
              .format(indicesinfo.count,  # count
                      "=" * 70,
                      indicesinfo.listinlines  # list with joined with "\n"
                      )
              )
    elif OPEN and DAYS is not None:
        indicestoopen = info.getIndicesToOpen(DAYS)
        print("Opening:\n{}".format('\n'.join(indicestoopen)))
        mod = Modify(es, indicestoopen)
        mod.Open()
    elif OPEN and INDEX is not None:
        print("Opening:\n{}".format('\n'.join(INDEX)))
        mod = Modify(es, INDEX)
        mod.Open()
    elif OPEN:
        openindicesinfo = info.getIndicesOpen()
        print("Open Indices: {}\n{}\n{}\n"
              .format(openindicesinfo.count,  # count
                      "=" * 70,
                      openindicesinfo.listinlines  # list with joined with "\n"
                      )
              )
    elif CLOSE and DAYS is not None:
        indicestoclose = info.getIndicesToClose(DAYS)
        print("Closing:\n{}".format('\n'.join(indicestoclose)))
        mod = Modify(es, indicestoclose)
        mod.Close()
    elif CLOSE and INDEX is not None:
        print("Closing:\n{}".format('\n'.join(INDEX)))
        mod = Modify(es, INDEX)
        mod.Close()
    elif CLOSE:
        closeindicesinfo = info.getIndicesClose()
        print("Close Indices: {}\n{}\n{}\n"
              .format(closeindicesinfo.count,  # count
                      "=" * 70,
                      closeindicesinfo.listinlines  # list joined with "\n"
                      )
              )


def snapCommands(es, args):
    REPO = args.repo
    LIST = args.list
    CREATE = args.create
    DELETE = args.delete
    if LIST:
        snap = Snapshot(es, REPO)
        print(snap.showSnap())
    if CREATE or DELETE:
        print("NOT IMPLEMENTED")


def repoCommands(es, args):
    LIST = args.list
    REPO = args.repo
    if LIST:
        repo = Repository(es, REPO)
        print(repo.listRepo())
    if REPO:
        print("NOT IMPLEMENTED")


def main():
    args = get_args()
    SERVER = args.server
    PORT = args.port
    is_reachable(SERVER, PORT)
    es = Elasticsearch(SERVER, port=PORT)
    info = Info(es)
    if args.parser_name == "indices":
        indicesCommands(es, info, args)
    elif args.parser_name == "snapshot":
        snapCommands(es, args)
    elif args.parser_name == "repo":
        repoCommands(es, args)

if __name__ == "__main__":
    main()
