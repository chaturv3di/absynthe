from __future__ import print_function
from typing import List
from random import randint
from datetime import datetime

from absynthe.cfg.graph import Graph
from absynthe.cfg.logger_node import LoggerNode


class SimpleBehavior(object):

    def __init__(self):
        self._cfgList: List[Graph] = list()
        self._fixedTimeDelta: float = 0.05
        return

    def addGraph(self, graph: Graph) -> None:
        self._cfgList.append(graph)
        return

    def synthesize(self, numRuns: int = 100):
        numGraphs: int = len(self._cfgList)
        nextNodeOf: List[LoggerNode] = None
        graphIdx: int = -1
        wallClock: float = -2.5
        for _ in range(numRuns):
            # Complete a traversal of each graph
            nextNodeOf = [self._cfgList[i].getRootAtRandom() for i in range(numGraphs)]
            toTraverse: int = len(nextNodeOf)
            wallClock += 2.5  # Just adding time delay between successive runs
            while 0 < toTraverse:
                graphIdx = randint(0, toTraverse - 1)
                timeStamp: str = str(datetime.fromtimestamp(wallClock))
                yield nextNodeOf[graphIdx].logInfo(timeStamp, None)
                wallClock += self._fixedTimeDelta

                nextNode: LoggerNode = nextNodeOf[graphIdx].getSuccessorAtRandom()
                if nextNode is None:
                    _ = nextNodeOf.pop(graphIdx)
                    toTraverse -= 1
                else:
                    nextNodeOf[graphIdx] = nextNode
