from __future__ import print_function
from typing import List
from random import randint
from datetime import datetime

from absynthe.cfg.graph import Graph
from absynthe.cfg.logger_node import LoggerNode

# Imports for Behavior
from abc import ABC, abstractmethod


class Behavior(ABC):

    @abstractmethod
    def addGraph(self, graph: Graph) -> None:
        pass

    @abstractmethod
    def synthesize(self, numRuns: int) -> None:
        pass


class MonospaceInterleaving(Behavior):

    def __init__(self, withSessions: bool = False):
        self._cfgList: List[Graph] = list()
        self._fixedTimeDelta: float = 0.05
        self._inclSessionID: bool = withSessions
        return

    def addGraph(self, graph: Graph) -> None:
        self._cfgList.append(graph)
        return

    def synthesize(self, numRuns: int = 100):
        numGraphs: int = len(self._cfgList)
        nextNodeOf: List[LoggerNode] = None
        graphIdx: int = -1
        wallClock: float = -2.5
        for i in range(numRuns):  # Complete a traversal of each graph
            nextNodeOf = [self._cfgList[i].getRootAtRandom() for i in range(numGraphs)]
            graphsAvailable = list(range(numGraphs))  # Shrinks as we reach the leaf of a graph
            toTraverse: int = numGraphs
            wallClock += 2.5  # Adding time delay between successive runs
            while 0 < toTraverse:
                # If there are still graphs available to traverse,
                # randomly choose a graph among those whose leaves
                # have not yet been reached in this run.
                posInGraphsAvailable: int = randint(0, toTraverse - 1)
                graphIdx: int = graphsAvailable[posInGraphsAvailable]
                graph: Graph = self._cfgList[graphIdx]

                timeStamp: str = str(datetime.fromtimestamp(wallClock))
                sessionID: str = ""
                if self._inclSessionID:
                    sessionID = "_".join(["SESSION", str(i), str(graphIdx)])

                # For the sake of better readability of logs, append
                # graph ID to the time stamp.
                logPrefix: str = " ".join([timeStamp, sessionID, graph.getID()])
                node: LoggerNode = nextNodeOf[graphIdx]
                yield node.logInfo(logPrefix, None)

                wallClock += self._fixedTimeDelta
                nextNode: LoggerNode = node.getSuccessorAtRandom()
                nextNodeOf[graphIdx] = nextNode
                if nextNode is None:
                    _ = graphsAvailable.pop(posInGraphsAvailable)
                    toTraverse -= 1
