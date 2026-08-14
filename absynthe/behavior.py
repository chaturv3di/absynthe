# Imports for Behavior
from abc import ABC, abstractmethod
from datetime import datetime
from random import randint, sample
from typing import cast

from .cfg import Graph, LoggerNode


class Behavior(ABC):

    @abstractmethod
    def addGraph(self, graph: Graph) -> None:
        pass

    @abstractmethod
    def synthesize(self, numRuns: int, withSessionID: bool) -> None:
        pass


class MonospaceSimple(Behavior):

    def __init__(self) -> None:
        self._cfgList: list[Graph] = list()
        self._fixedTimeDelta: float = 0.05
        return

    def addGraph(self, graph: Graph) -> None:
        self._cfgList.append(graph)
        return

    def synthesize(self, numRuns: int = 100, withSessionID: bool = False):
        numGraphs: int = len(self._cfgList)
        graphIdx: int = -1
        wallClock: float = -2.5
        for i in range(numRuns):  # Complete a traversal of each graph
            graphOrder: list[int] = sample(range(numGraphs), numGraphs)
            wallClock += 2.5  # Adding time delay between successive runs
            for graphIdx in graphOrder:
                graph: Graph = self._cfgList[graphIdx]
                node: LoggerNode | None = cast(LoggerNode, graph.getRootAtRandom())

                while node is not None:
                    timeStamp: str = str(datetime.fromtimestamp(wallClock))
                    sessionID: str = ""
                    if withSessionID:
                        sessionID = "_".join(["SESSION", str(i), str(graphIdx)])

                    # For the sake of better readability of logs, append
                    # graph ID to the time stamp.
                    logPrefix: str = " ".join([timeStamp, sessionID, graph.getID()])
                    yield node.logInfo(logPrefix, None)

                    wallClock += self._fixedTimeDelta
                    node = cast("LoggerNode | None", node.getSuccessorAtRandom())


class MonospaceInterleaving(Behavior):

    def __init__(self) -> None:
        self._cfgList: list[Graph] = list()
        self._fixedTimeDelta: float = 0.05
        return

    def addGraph(self, graph: Graph) -> None:
        self._cfgList.append(graph)
        return

    def synthesize(self, numRuns: int = 100, withSessionID: bool = False):
        numGraphs: int = len(self._cfgList)
        nextNodeOf: list[LoggerNode | None] | None = None
        graphIdx: int = -1
        wallClock: float = -2.5
        for i in range(numRuns):  # Complete a traversal of each graph
            nextNodeOf = [cast(LoggerNode, self._cfgList[i].getRootAtRandom())
                         for i in range(numGraphs)]
            graphsAvailable = list(range(numGraphs))  # Shrinks as we reach the leaf of a graph
            toTraverse: int = numGraphs
            wallClock += 2.5  # Adding time delay between successive runs
            while 0 < toTraverse:
                # If there are still graphs available to traverse,
                # randomly choose a graph among those whose leaves
                # have not yet been reached in this run.
                posInGraphsAvailable: int = randint(0, toTraverse - 1)
                graphIdx = graphsAvailable[posInGraphsAvailable]
                graph: Graph = self._cfgList[graphIdx]

                timeStamp: str = str(datetime.fromtimestamp(wallClock))
                sessionID: str = ""
                if withSessionID:
                    sessionID = "_".join(["SESSION", str(i), str(graphIdx)])

                # For the sake of better readability of logs, append
                # graph ID to the time stamp.
                logPrefix: str = " ".join([timeStamp, sessionID, graph.getID()])
                node: LoggerNode = cast(LoggerNode, nextNodeOf[graphIdx])
                yield node.logInfo(logPrefix, None)

                wallClock += self._fixedTimeDelta
                nextNode: LoggerNode | None = cast("LoggerNode | None",
                                                   node.getSuccessorAtRandom())
                nextNodeOf[graphIdx] = nextNode
                if nextNode is None:
                    _ = graphsAvailable.pop(posInGraphsAvailable)
                    toTraverse -= 1
