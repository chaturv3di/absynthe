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

# Imports for TreeBuilder
from time import ctime
from importlib import import_module
from random import sample


class GraphBuilder(ABC):
    """
    The abstract base class for all kinds of graph builders. Each graph builder object takes
    keyword arguments to initialise itself. The base class only specifies one method,
    `generateNewGraph()`, which should be able to generate a *new* graph with every invocation
    (subject to the initialising parameters).
    """

    # Node module
    LOGGER_NODE_MODULE = "absynthe.cfg.logger_node"

    # Keywords for the kwargs expected by the constructor
    KW_NUM_ROOTS = "NUM_ROOTS"
    KW_NUM_LEAVES = "NUM_LEAVES"
    KW_MIN_NUM_INNER_NODES = "MIN_NUM_INNER_NODES"
    KW_MAX_NUM_INNER_NODES = "MAX_NUM_INNER_NODES"
    KW_BRANCHING_DEGREE = "BRANCHING_DEGREE"
    KW_SUPPORTED_NODE_TYPES = "SUPPORTED_NODE_TYPES"

    def __init__(self, **kwargs: str) -> None:
        """
        Construtor for the class.
        Args:
          **kwargs(str): Must have the following keywords.
            KW_NUM_ROOTS - specifying the number of roots in any graph this builder creates.
            KW_NUM_LEAVES - specifying the number of leaves that any graph can have.
            KW_MIN_NUM_INNER_NODES - Besides roots and leaves, the min number of inner nodes.
            KW_MAX_NUM_INNER_NODES - Besides roots and leaves, the max number of inner nodes.
            KW_BRANCHING_DEGREE - Approximate branching factor for each node.
            KW_SUPPORTED_NODE_TYPES - Concrete LoggerNode types that can be part of graphs.
        """
        # Fields that would be initialised from user input.
        # Failure to initialise any one of these will raise an error.
        self._numRoots: int = 0
        self._numLeaves: int = 0
        self._minNumInnerNodes: int = 0
        self._maxNumInnerNodes: int = 0
        self._branchingDegree: int = 0
        self._deltaRange: int = 0
        self._supportedNodeTypes: List[str] = None
        self._rootList: List[Node] = None

        try:
            self._numRoots = int(kwargs[GraphBuilder.KW_NUM_ROOTS])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Number of roots must be specified using the key ",
                  "GraphBuilder.KW_NUM_ROOTS.",
                  file=stderr)
            raise ke

        try:
            self._numLeaves = int(kwargs[GraphBuilder.KW_NUM_LEAVES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Number of leaves must be specified using the key ",
                  "GraphBuilder.KW_NUM_LEAVES.",
                  file=stderr)
            raise ke

        try:
            self._minNumInnerNodes = int(kwargs[GraphBuilder.KW_MIN_NUM_INNER_NODES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Minimum number of inner nodes must be specified using the key ",
                  "GraphBuilder.KW_MIN_NUM_INNER_NODES.",
                  file=stderr)
            raise ke

        try:
            self._maxNumInnerNodes = int(kwargs[GraphBuilder.KW_MAX_NUM_INNER_NODES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Maximum number of inner nodes must be specified using the key ",
                  "GraphBuilder.KW_MAX_NUM_INNER_NODES.",
                  file=stderr)
            raise ke

        try:
            self._branchingDegree = int(kwargs[GraphBuilder.KW_BRANCHING_DEGREE])
            self._deltaRange = self._branchingDegree // 2
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Approx. branching degree must be specified using the key ",
                  "GraphBuilder.KW_BRANCHING_DEGREE.",
                  file=stderr)
            raise ke

        try:
            self._supportedNodeTypes = [x.strip()
                                        for x in
                                        kwargs[GraphBuilder.KW_SUPPORTED_NODE_TYPES].split(',')]
        except KeyError as ke:
            print(type(self).__name__,
                  "ERROR- Types of nodes supported in this graph must be specified using the key ",
                  "GraphBuilder.KW_SUPPORTED_NODE_TYPES as comma-separated list of class names.",
                  file=stderr)
            raise ke

        self._coreNodeClasses = list()
        for name, obj in inspect.getmembers(modules["absynthe.cfg.node"], inspect.isclass):
            if not inspect.isabstract(obj) and not name == "ABC":
                self._coreNodeClasses.append(name)

        # Everything okay, so instantiate object
        return

    def _generateID(self, entityType: str, nodeNum: int, timeStamp: str) -> str:
        return "::".join([entityType, str(nodeNum)])

    def _newRandomNode(self, id: str) -> Node:
        loggerNodeModule = import_module(GraphBuilder.LOGGER_NODE_MODULE)
        loggerNodeClassName = self._supportedNodeTypes[randint(0, len(self._supportedNodeTypes) - 1)]
        coreNodeClassName = self._coreNodeClasses[randint(0, len(self._coreNodeClasses) - 1)]
        logger_kwargs = {LoggerNode.KW_CORE_CLASS_NAME: coreNodeClassName,
                         LoggerNode.KW_IGNORE_PARAMS: "False"}
        TreeBuilder.numNodes += 1
        return getattr(loggerNodeModule, loggerNodeClassName)(id, **logger_kwargs)

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

    def size(self) -> int:
        return self._numNodes

    @abstractmethod
    def generateNewGraph(self) -> Graph:
        """
        Generates a new graph adhering to the arguments specified by the kwargs
        in the constructor. Each invocation of this method can potentially
        generate a different graph.
        """
        pass


class TreeBuilder(GraphBuilder):

    numGraphs: int = 0
    numNodes: int = 0

    def __init__(self, **kwargs: str) -> None:
        super().__init__(**kwargs)
        return

    def generateNewGraph(self) -> Graph:
        TreeBuilder.numGraphs += 1
        self._nodeLayers: List[List[Node]] = list()

        # 1. Create Graph ID.
        timeStamp: str = ctime()
        graphID: str = self._generateID("graph", TreeBuilder.numGraphs, timeStamp)
        graph: Graph = Graph(graphID, self._numRoots)

        # 2. Create desired no. of roots.
        rootLayer: List[Node] = list()
        for _ in range(self._numRoots):
            nodeID: str = self._generateID("root", TreeBuilder.numNodes, timeStamp)
            rNode = self._newRandomNode(nodeID)
            graph.addRoot(rNode)
            rootLayer.append(rNode)
        self._nodeLayers.append(rootLayer)

        balNumInnerNodes: int = randint(self._minNumInnerNodes, self._maxNumInnerNodes)
        # 3. For each currLayer, starting with roots
        currLayer: List[Node] = rootLayer
        nextLayer: List[Node] = [None] * self._numRoots * (self._branchingDegree + self._deltaRange)
        while(nextLayer is not None):
            balNumInnerNodes -= self._makeConnections(currLayer, nextLayer, timeStamp)
            try:
                while(True):
                    nextLayer.remove(None)
            except ValueError:
                self._nodeLayers.append(nextLayer)
                currLayer = nextLayer

            if (0 >= balNumInnerNodes):
                nextLayer = None
            else:
                nextLayer = [None] * len(currLayer) * (self._branchingDegree + self._deltaRange)

        # 4. Create desired no. of leaves (nodes with `None` successors)
        leafLayer: List[Node] = list()
        for _ in range(self._numRoots):
            nodeID: str = self._generateID("leaf", TreeBuilder.numNodes, timeStamp)
            leafLayer.append(self._newRandomNode(nodeID))
        _ = self._makeConnections(currLayer, leafLayer, timeStamp, True)
        self._nodeLayers.append(leafLayer)

        return graph

    def _makeConnections(self, fromLayer: List[Node], toLayer: List[Node],
                         timeStamp: str, toLeafLayer: bool = False) -> int:
        numNodes: int = 0
        for node in fromLayer:
            if toLeafLayer:
                succPositions = range(len(toLayer))
            else:
                succPositions = sample(range(len(toLayer)), self._howManySuccessors())

            for succPos in succPositions:
                succNode: Node = toLayer[succPos]
                if succNode is None:
                    succNode = self._newRandomNode(self._generateID("node",
                                                                    TreeBuilder.numNodes,
                                                                    timeStamp))
                    toLayer[succPos] = succNode
                    numNodes += 1
                node.addSuccessor(succNode)
        return numNodes


class DAGBuilder(TreeBuilder):

    def __init__(self, **kwargs: str) -> None:
        super().__init__(**kwargs)
        return

    def generateNewGraph(self) -> Graph:
        # 1. super().generateNewGraph()
        # 2. Randomly add skip edges, i.e. from layer_i to layer_>(i + 1)
        return None


class GraphBuilder(DAGBuilder):

    def __init__(self, **kwargs: str) -> None:
        super().__init__(**kwargs)
        return

    def generateNewGraph(self) -> Graph:
        # 1. super().generateNewGraph()
        # 2. Randomly add few reverse edges
        # 3. Add loops
        return None
