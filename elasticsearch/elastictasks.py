#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-10-11T21:17:52-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-10-19T21:11:43-04:00

from elasticsearch import Elasticsearch
import elasticsearch.exceptions as Exceptions
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
        if len(data) == 0:
            print("No indices to Open for indicated range.")
            sys.exit(1)
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
            try:
                [health, status, index, pri, rep,
                    docs_count, docs_deleted, store_size,
                    pri_store_size] = x.split(" ")
                datestamp = "".join(index.split("-")[-1:])
                index_date = datetime.strptime(str(datestamp), "%Y.%m.%d")
                diff = datetime.now() - index_date
                if diff.days > days:
                    toclose.append(index)
            except Exception:
                print("No indices to Close for indicated range.")
                sys.exit(1)
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
        repository = self.repo
        snapshot = self.snapname
        INDICES = ", ".join(self.idxlist)
        data = {}
        data["indices"] = INDICES
        data["ignore_unavailable"] = "true"
        data["include_global_state"] = "false"
        json_data = json.dumps(data)
        self.esinst.snapshot.create(repository=repository,
                                    snapshot=snapshot, body=json_data)

    def deleteSnap(self):
        repository = self.repo
        snapshot = self.snapname
        self.esinst.snapshot.delete(repository=repository,
                                    snapshot=snapshot)


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
        help="Elasticsearch Port",
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
    snapgroup1.add_argument("--create", action="store",
                            help="Create Snapshot")
    snapgroup1.add_argument("--delete", action="store", help="Delete Snapshot")
    snap.add_argument("-i", "--index", action="store",
                      help="List of indices for Snap", nargs="+")
    # Parser for repositories
    repo = subparserrepo.add_parser("repository",
                                    help="Actions with repositories")
    repo.add_argument("-l", "--list", action="store_true")
    repo.add_argument("--repo", action="store")

    args = parser.parse_args()
    return args


def indicesCommands(es, info, args):
    LIST = args.list
    OPEN = args.open
    CLOSE = args.close
    INDEX = args.index
    DAYS = args.days
    if LIST:
        indicesinfo = info.getIndices()
        print("Indices: {}\n{}\n{}\n"
              .format(indicesinfo.count,  # count
                      "=" * 70,
                      indicesinfo.listinlines  # list joined with "\n"
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
                      openindicesinfo.listinlines  # list joined with "\n"
                      )
              )
    elif CLOSE and DAYS is not None:
        indicestoclose = info.getIndicesToClose(DAYS)
        if len(indicestoclose) == 0:
            print("No indices to close for specified range.")
            sys.exit(1)
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
    else:
        print("Missing options")


def snapCommands(es, args):
    REPO = args.repo
    LIST = args.list
    CREATE = args.create
    DELETE = args.delete
    if LIST:
        snap = Snapshot(es, REPO)
        try:
            print(snap.showSnap())
        except Exceptions.NotFoundError as err:
            print("Error: Repo not found.\n{}".format(err))
    elif CREATE and args.index is not None:
        INDICES = args.index
        # To avoid leaving indices out of the snapshot, we are converting the
        # indices input.
        #
        # elastictask.py -s SERVER snapshot --repo archives \
        # --create snapshot_test1 --index INDEX1 INDEX2
        # the returned arg for INDICES is ["INDEX1", "INDEX2"]
        # This arg will FAIL.
        #
        # elastictask.py -s SERVER snapshot --repo archives \
        # --create snapshot_test1 --index INDEX1,INDEX2
        # the returned arg for INDICES is ["INDEX1,INDEX2"]
        # This arg will WORK.
        if len(INDICES) > 1:
            joined = [",".join(INDICES)]
            INDICES = joined
        SNAP = args.create
        try:
            Snapshot(es, REPO, snapname=SNAP, idxlist=INDICES).createSnap()
        except Exceptions.RequestError as err:
            print("Error: Duplicated snapshot name.\n{}".format(err))
            sys.exit(1)
        except Exceptions.AuthorizationException as err:
            print("Error: index closed.\n{}".format(err))
            sys.exit(1)
        print("Creating Snapshot for:\n{}".format(INDICES))
    elif CREATE and args.index is None:
        print("You must indicate the indices for the snapshot."
              " (--index index1 index2  or --index index1,index2)")
    elif DELETE and args.index is not None:
        print("Can't mix delete snapshot with indices")
    elif DELETE:
        SNAP = args.delete
        try:
            print("Deleting snapshot: {} in repository: {}"
                  .format(SNAP, REPO))
            Snapshot(es, REPO, snapname=SNAP).deleteSnap()
        except Exceptions.TransportError as err:
            print("Error: Snapshot not found.\n{}".format(err))
    else:
        print("Missing options")


def repoCommands(es, args):
    LIST = args.list
    REPO = args.repo
    if LIST:
        repo = Repository(es, REPO)
        print(repo.listRepo())
    elif REPO:
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
    elif args.parser_name == "repository":
        repoCommands(es, args)

if __name__ == "__main__":
    main()
