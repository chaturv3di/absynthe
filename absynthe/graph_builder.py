from __future__ import print_function
from sys import stderr
from typing import List
from random import randint

# Local imports
from .cfg.node import Node
from .cfg.logger_node import LoggerNode
from .cfg.graph import Graph

# Imports for GraphBuilder
from abc import ABC, abstractmethod
from sys import modules
import inspect

# Imports for concrete builders
from collections import defaultdict
from importlib import import_module
from random import sample
from math import ceil


class GraphBuilder(ABC):
    """
    The abstract base class for all kinds of graph builders. Each graph builder object takes
    keyword arguments to initialise itself. The base class only specifies one method,
    `generateNewGraph()`, which should be able to generate a *new* graph with every invocation
    (subject to the initialising parameters).

    This class can be extended in two ways:

    1. As illustrated by the TreeBuilder class and its subclasses, implementations that take
       a number of arguments and randomly create new graphs.
    2. TODO: Implementations that read hand-crafted specifications and creates graphs that
       meet those specs.
    """

    def __init__(self, **kwargs: str) -> None:
        pass

    @abstractmethod
    def generateNewGraph(self, **kwargs: str) -> Graph:
        """
        Generates a new graph adhering to the arguments specified by the kwargs
        in the constructor. Each invocation of this method can potentially
        generate a different graph.
        """
        pass


class TreeBuilder(GraphBuilder):

    numGraphs: int = 0
    numNodes: int = 0

    # Keywords for the kwargs expected by the constructor
    KW_NUM_ROOTS = "NUM_ROOTS"
    KW_NUM_LEAVES = "NUM_LEAVES"
    KW_NUM_INNER_NODES = "NUM_INNER_NODES"
    KW_BRANCHING_DEGREE = "BRANCHING_DEGREE"
    KW_SUPPORTED_NODE_TYPES = "SUPPORTED_NODE_TYPES"

    # Node module
    LOGGER_NODE_MODULE = "absynthe.cfg.logger_node"

    def __init__(self, **kwargs: str) -> None:
        """
        Construtor for the class.
        Args:
          **kwargs(str): Must have the following keywords.
            KW_NUM_ROOTS - specifying the number of roots in any graph this builder creates.
            KW_NUM_LEAVES - specifying the number of leaves that any graph can have.
            KW_NUM_INNER_NODES - Besides roots and leaves, the approx. number of inner nodes.
            KW_BRANCHING_DEGREE - Approximate branching factor for each node.
            KW_SUPPORTED_NODE_TYPES - Concrete LoggerNode types that can be part of graphs.
        """
        # Fields that would be initialised from user input.
        # Failure to initialise any one of these will raise an error.
        self._numRoots: int = 0
        self._numLeaves: int = 0
        self._numInnerNodes: int = 0
        self._branchingDegree: int = 0
        self._deltaRange: int = 0
        self._supportedNodeTypes: List[str] = None
        self._rootList: List[Node] = None

        try:
            self._numRoots = int(kwargs[TreeBuilder.KW_NUM_ROOTS])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Number of roots must be specified using the key ",
                  "TreeBuilder.KW_NUM_ROOTS.",
                  file=stderr)
            raise ke

        try:
            self._numLeaves = int(kwargs[TreeBuilder.KW_NUM_LEAVES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Number of leaves must be specified using the key ",
                  "TreeBuilder.KW_NUM_LEAVES.",
                  file=stderr)
            raise ke

        try:
            self._numInnerNodes = int(kwargs[TreeBuilder.KW_NUM_INNER_NODES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Number of inner nodes must be specified using the key ",
                  "TreeBuilder.KW_NUM_INNER_NODES.",
                  file=stderr)
            raise ke

        try:
            self._branchingDegree = int(kwargs[TreeBuilder.KW_BRANCHING_DEGREE])
            self._deltaRange = self._branchingDegree // 2
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Approx. branching degree must be specified using the key ",
                  "TreeBuilder.KW_BRANCHING_DEGREE.",
                  file=stderr)
            raise ke

        try:
            self._supportedNodeTypes = [x.strip()
                                        for x in
                                        kwargs[TreeBuilder.KW_SUPPORTED_NODE_TYPES].split(',')]
        except KeyError as ke:
            print(type(self).__name__,
                  "ERROR- Types of nodes supported in this graph must be specified using the key ",
                  "TreeBuilder.KW_SUPPORTED_NODE_TYPES as comma-separated list of class names.",
                  file=stderr)
            raise ke

        self._coreNodeClasses = list()
        for name, obj in inspect.getmembers(modules["absynthe.cfg.node"], inspect.isclass):
            if not inspect.isabstract(obj) and not name == "ABC":
                self._coreNodeClasses.append(name)

        self._loggerNodeModule = import_module(TreeBuilder.LOGGER_NODE_MODULE)
        # Everything okay, so instantiate object
        return

    def _generateID(self, entityType: str, nodeNum: int) -> str:
        return "::".join([entityType, str(nodeNum)])

    def _newRandomNode(self, eType: str) -> Node:
        id = self._generateID(eType, TreeBuilder.numNodes)
        loggerNodeClassName = self._supportedNodeTypes[randint(0, len(self._supportedNodeTypes) - 1)]
        coreNodeClassName = self._coreNodeClasses[randint(0, len(self._coreNodeClasses) - 1)]
        logger_kwargs = {LoggerNode.KW_CORE_CLASS_NAME: coreNodeClassName,
                         LoggerNode.KW_IGNORE_PARAMS: "False"}
        TreeBuilder.numNodes += 1
        return getattr(self._loggerNodeModule, loggerNodeClassName)(id, **logger_kwargs)

    def _howManySuccessors(self, succLimit: int = None) -> int:
        """
        Randomly generate the number indicating how many successors a node will have. The
        following possibilities are equally likely:
        1. One successor
        2. Two successors
        3. (BRANCHING_DEGREE +/- delta) successors
        Returns:
          int: The number of successors a node will have
        """
        if succLimit is not None:
            return randint(0, succLimit - 1)

        theseMany: int = randint(1, 3)
        if 3 > theseMany:
            return theseMany

        delta: int = randint(-self._deltaRange, self._deltaRange)
        theseMany = self._branchingDegree + delta
        return theseMany

    def _makeConnections(self, fromLayer: List[Node], toLayer: List[Node],
                         toLeafLayer: bool = False) -> int:
        """
        Except when toLeafLayer is True, it is possible that some of the nodes in toLayer
        have no predecessors from fromLayer assigned to them at the end of this method.
        Such nodes might have to be explicitly removed after returning from here.
        """
        numNodes: int = 0
        leavesCovered: defaultdict = defaultdict(bool)
        sizeToLayer: int = len(toLayer)
        maxLeavesPerNode: int = min(2, sizeToLayer)
        for node in fromLayer:
            if toLeafLayer:
                # Select at most maxLeavesPerNode successors
                succPositions = sample(range(sizeToLayer), randint(1, maxLeavesPerNode))
            else:
                # Select successor positions randomly
                succPositions = sample(range(sizeToLayer), self._howManySuccessors())

            for succPos in succPositions:
                # Make connections between fromLayer and toLayer
                succNode: Node = toLayer[succPos]
                if succNode is None:
                    succNode = self._newRandomNode("node")
                    toLayer[succPos] = succNode
                    numNodes += 1
                node.addSuccessor(succNode)
                leavesCovered[succPos] = True
            # At the end of the loop, it is possible that some nodes in toLayer have no
            # predecessor nodes in fromLayer. In this case, the corresponding succPositions
            # in toLayer would continue to have None elements.

        if toLeafLayer:
            # If toLayer is the leaf layer, then we want to ensure that all leaf nodes have
            # at least one predecessor node.
            sizeFromLayer: int = len(fromLayer)
            for succPos in set(range(sizeToLayer)).difference(leavesCovered.keys()):
                randomFromPos = randint(0, sizeFromLayer - 1)
                fromLayer[randomFromPos].addSuccessor(toLayer[succPos])
                numNodes += 1
        return numNodes

    def generateNewGraph(self) -> Graph:
        TreeBuilder.numGraphs += 1
        self._nodeLayers: List[List[Node]] = list()

        # 1. Create Graph ID.
        graphID: str = self._generateID("graph", TreeBuilder.numGraphs)
        graph: Graph = Graph(graphID, self._numRoots)

        # 2. Create desired no. of roots.
        rootLayer: List[Node] = list()
        for _ in range(self._numRoots):
            rNode = self._newRandomNode("root")
            graph.addRoot(rNode)
            rootLayer.append(rNode)
        self._nodeLayers.append(rootLayer)

        balNumInnerNodes: int = self._numInnerNodes
        # 3. For each currLayer, starting with roots
        currLayer: List[Node] = rootLayer
        nextLayer: List[Node] = [None] * self._numRoots * (self._branchingDegree + self._deltaRange)
        while(nextLayer is not None):
            balNumInnerNodes -= self._makeConnections(currLayer, nextLayer)
            try:
                # Since some of the nodes in nextLayer were not assigned any predecessors
                # from the currLayer, we simply remove those None values.
                while(True):
                    nextLayer.remove(None)
            except ValueError:
                # nextLayer is free from None nodes
                self._nodeLayers.append(nextLayer)
                currLayer = nextLayer

            if (0 >= balNumInnerNodes):
                nextLayer = None
            else:
                nextLayer = [None] * len(currLayer) * (self._branchingDegree + self._deltaRange)

        # 4. Create desired no. of leaves (nodes with `None` successors)
        leafLayer: List[Node] = list()
        for _ in range(self._numLeaves):
            leafLayer.append(self._newRandomNode("leaf"))
        _ = self._makeConnections(currLayer, leafLayer, True)
        self._nodeLayers.append(leafLayer)

        return graph


class DAGBuilder(TreeBuilder):
    """
    Directed Acyclic Graph Builder class
    """

    def __init__(self, **kwargs: str) -> None:
        super().__init__(**kwargs)
        # A graph with N layers will contain (N // _skipFraction) skip edges
        self._skipFraction: int = 3
        return

    def generateNewGraph(self) -> Graph:
        # 1. super().generateNewGraph()
        # 2. Randomly add skip edges, i.e. from layer_i to layer_>(i + 1)
        graph: Graph = super().generateNewGraph()

        numLevels: int = len(self._nodeLayers)
        if 4 > numLevels:
            return graph

        # Randomly choose levels from where some node will have an outgoing skip-edge
        fromLevels: List[int] = sample(range(numLevels - 2),
                                       numLevels // self._skipFraction)
        numNodesInLevel: int = 0
        for level in fromLevels:
            # For each level in the random list created above,
            # select a random node from which a skip-edge will
            # start
            numNodesInLevel = len(self._nodeLayers[level])
            fromNode: Node = self._nodeLayers[level][randint(0, numNodesInLevel - 1)]
            # Randomly select a lower level at which the skip-
            # edge will terminate
            toLevel: int = randint(level + 2, numLevels - 1)
            numNodesInLevel = len(self._nodeLayers[toLevel])
            # In the said lower level, randomly select a node
            # that will receive the skip-edge
            toNode: Node = self._nodeLayers[toLevel][randint(0, numNodesInLevel - 1)]
            fromNode.addSuccessor(toNode)
        return graph


class DCGBuilder(DAGBuilder):
    """
    Directed Cyclic Graph Builder class
    """

    def __init__(self, **kwargs: str) -> None:
        super().__init__(**kwargs)
        # If a graph has N inner nodes, then (N // _loopFraction) nodes will
        # be set aside to appear in loops.
        self._loopFraction = 5
        self._numLoopNodes = ceil(self._numInnerNodes / self._loopFraction)
        self._numInnerNodes -= self._numLoopNodes
        return

    def _attachLoop(self, toNode: Node, ofSize: int) -> None:
        entityType: str = "loop_" + toNode.getID()
        currNode: Node = toNode
        loopNode: Node = None
        for _ in range(ofSize):
            loopNode = self._newRandomNode(entityType)
            currNode.addSuccessor(loopNode)
            currNode = loopNode

        currNode.addSuccessor(toNode)
        return

    def generateNewGraph(self) -> Graph:
        # 1. super().generateNewGraph()
        # 2. Randomly add few reverse edges
        # 3. Add loops
        graph: Graph = super().generateNewGraph()
        numLevels: int = len(self._nodeLayers)
        if 3 > numLevels:
            return graph

        numNodesPerLoop: int = 3  # FIXED FOR NOW
        numLoops: int = ceil(self._numLoopNodes / numNodesPerLoop)
        for _ in range(numLoops):
            level: int = randint(1, numLevels - 2)
            nodeNum: int = randint(0, len(self._nodeLayers[level]) - 1)
            toNode: Node = self._nodeLayers[level][nodeNum]
            self._attachLoop(toNode, numNodesPerLoop)

        return graph
