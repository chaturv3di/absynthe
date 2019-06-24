from __future__ import print_function
from sys import stderr
from typing import List
from random import randint

# Local imports
from .cfg import Node, Graph
from .cfg.utils import Utils

# Imports for GraphBuilder
from abc import ABC, abstractmethod
from sys import modules
import inspect

# Imports for concrete graph builders
from collections import defaultdict
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

        className: str = type(self).__name__
        try:
            self._numRoots = int(kwargs[TreeBuilder.KW_NUM_ROOTS])
        except KeyError as ke:
            print(className,
                  "ERROR - Number of roots must be specified using the key",
                  className, "\b.KW_NUM_ROOTS.",
                  file=stderr)
            raise ke

        try:
            self._numLeaves = int(kwargs[TreeBuilder.KW_NUM_LEAVES])
        except KeyError as ke:
            print(className,
                  "ERROR - Number of leaves must be specified using the key",
                  className, "\b.KW_NUM_LEAVES.",
                  file=stderr)
            raise ke

        try:
            self._numInnerNodes = int(kwargs[TreeBuilder.KW_NUM_INNER_NODES])
        except KeyError as ke:
            print(className,
                  "ERROR - Number of inner nodes must be specified using the key",
                  className, "\b.KW_NUM_INNER_NODES.",
                  file=stderr)
            raise ke

        try:
            self._branchingDegree = int(kwargs[TreeBuilder.KW_BRANCHING_DEGREE])
            self._deltaRange = self._branchingDegree // 2
        except KeyError as ke:
            print(className,
                  "ERROR - Approx. branching degree must be specified using the key",
                  className, "\b.KW_BRANCHING_DEGREE.",
                  file=stderr)
            raise ke

        try:
            self._supportedNodeTypes = [x.strip()
                                        for x in
                                        kwargs[TreeBuilder.KW_SUPPORTED_NODE_TYPES].split(',')]
        except KeyError as ke:
            print(className,
                  "ERROR- Types of nodes supported in this graph must be specified using the key",
                  className, "\b.KW_SUPPORTED_NODE_TYPES as comma-separated list of class names.",
                  file=stderr)
            raise ke

        self._coreNodeClasses = list()
        for name, obj in inspect.getmembers(modules["absynthe.cfg.node"], inspect.isclass):
            if not inspect.isabstract(obj) and not name == "ABC":
                self._coreNodeClasses.append(name)

        # Everything okay, so instantiate object
        return

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
                succNodeID: str
                if succNode is None:
                    succNodeID = Utils.generateID("node", TreeBuilder.numNodes)
                    succNode = Utils.newRandomNode(succNodeID,
                                                   self._supportedNodeTypes,
                                                   self._coreNodeClasses)
                    TreeBuilder.numNodes += 1
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
        """
        Returns:
          Graph: A tree-like graph, which mostly satisfies the specifications provided
                 in the constructor.
        """
        TreeBuilder.numGraphs += 1
        self._nodeLayers: List[List[Node]] = list()

        # 1. Create Graph ID.
        graphID: str = Utils.generateID("graph", TreeBuilder.numGraphs)
        graph: Graph = Graph(graphID, self._numRoots)

        # 2. Create desired no. of roots.
        rootLayer: List[Node] = list()
        for _ in range(self._numRoots):
            rNodeID = Utils.generateID("root", TreeBuilder.numNodes,)
            rNode = Utils.newRandomNode(rNodeID,
                                        self._supportedNodeTypes,
                                        self._coreNodeClasses)
            TreeBuilder.numNodes += 1
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
            lNodeID = Utils.generateID("leaf", TreeBuilder.numNodes)
            leafLayer.append(Utils.newRandomNode(lNodeID,
                                                 self._supportedNodeTypes,
                                                 self._coreNodeClasses))
            TreeBuilder.numNodes += 1
        _ = self._makeConnections(currLayer, leafLayer, True)
        self._nodeLayers.append(leafLayer)

        return graph


class DAGBuilder(TreeBuilder):
    """
    Directed Acyclic Graph Builder class
    """

    def __init__(self, **kwargs: str) -> None:
        """
        Construtor for the class takes exactly the same keyword arguments as TreeBuilder.
        Args:
          **kwargs(str): Must have the following keywords.
            KW_NUM_ROOTS - specifying the number of roots in any graph this builder creates.
            KW_NUM_LEAVES - specifying the number of leaves that any graph can have.
            KW_NUM_INNER_NODES - Besides roots and leaves, the approx. number of inner nodes.
            KW_BRANCHING_DEGREE - Approximate branching factor for each node.
            KW_SUPPORTED_NODE_TYPES - Concrete LoggerNode types that can be part of graphs.
        """
        super().__init__(**kwargs)
        # A graph with N layers will contain (N // _skipFraction) skip edges
        self._skipFraction: int = 3
        return

    def generateNewGraph(self) -> Graph:
        """
        This method first constructs a tree using the super class' generateNewGraph()
        method, and then adds some skip-level edges. Skip-level edges are edges that
        originate at a node on some level `i` and terminate at a node at some level
        `> (i + 1)`.

        Skip-level edges are only added to the graph if there are enough inner nodes to
        allow more than three levels.

        Returns:
          Graph: A directed acyclic graph, which mostly satisfies the specifications
                 provided in the constructor.
        """
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

    # Additional keyword(s) for the kwargs expected by the constructor
    KW_REVERSE_EDGES = "REVERSE_EDGES"

    def __init__(self, **kwargs: str) -> None:
        """
        Construtor for the class takes all the keyword arguments of the super(-super) class
        TreeBuilder, and an additional one.
        Args:
          **kwargs(str): Must have the following keywords.
            KW_NUM_ROOTS - specifying the number of roots in any graph this builder creates.
            KW_NUM_LEAVES - specifying the number of leaves that any graph can have.
            KW_NUM_INNER_NODES - Besides roots and leaves, the approx. number of inner nodes.
            KW_BRANCHING_DEGREE - Approximate branching factor for each node.
            KW_SUPPORTED_NODE_TYPES - Concrete LoggerNode types that can be part of graphs.

            KW_REVERSE_EDGES - specifying whether or not there should be edges in the
                               "upward" direction, i.e. *to* level `i` *from* some level
                               `>i`. Reverse edges are only constructed if the graph has more
                               than 3 level.
        """
        super().__init__(**kwargs)

        self._reverseEdges: bool = False
        try:
            self._reverseEdges = bool(kwargs[DCGBuilder.KW_REVERSE_EDGES])
        except KeyError:
            self._reverseEdges = False
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
            lNodeID = Utils.generateID(entityType, DCGBuilder.numNodes)
            loopNode = Utils.newRandomNode(lNodeID,
                                           self._supportedNodeTypes,
                                           self._coreNodeClasses)
            DCGBuilder.numNodes += 1
            currNode.addSuccessor(loopNode)
            currNode = loopNode

        currNode.addSuccessor(toNode)
        return

    def generateNewGraph(self) -> Graph:
        """
        This method first constructs a DAG using the super class' generateNewGraph()
        method, and then adds loops and (optionally) reverse edges.

        Loops and reverse edges can only be added to a graph if there are enough
        inner nodes to allow more than three levels.

        Returns:
          Graph: A directed cyclic graph, which mostly satisfies the specifications
                 provided in the constructor.
        """
        # 1. super().generateNewGraph()
        graph: Graph = super().generateNewGraph()

        numLevels: int = len(self._nodeLayers)
        if 3 > numLevels:
            return graph

        # 2. Add loops
        numNodesPerLoop: int = 3  # FIXED FOR NOW
        numLoops: int = ceil(self._numLoopNodes / numNodesPerLoop)
        for _ in range(numLoops):
            level: int = randint(1, numLevels - 2)
            nodeNum: int = randint(0, len(self._nodeLayers[level]) - 1)
            toNode: Node = self._nodeLayers[level][nodeNum]
            self._attachLoop(toNode, numNodesPerLoop)

        if not self._reverseEdges:
            return graph

        # 3. Randomly add few reverse edges
        fromLevels: List[int] = sample(range(2, numLevels - 1),
                                       numLevels // self._skipFraction)
        for level in fromLevels:
            # For each level in the random list created above,
            # select a random node from which a reverse edge
            # will start
            numNodesInLevel = len(self._nodeLayers[level])
            fromNode: Node = self._nodeLayers[level][randint(0, numNodesInLevel - 1)]
            # Randomly select an upper level at which the
            # reverse edge will terminate
            toLevel: int = randint(0, level - 2)
            numNodesInLevel = len(self._nodeLayers[toLevel])
            # In the said upper level, randomly select a node
            # that will receive the skip-edge
            toNode: Node = self._nodeLayers[toLevel][randint(0, numNodesInLevel - 1)]
            fromNode.addSuccessor(toNode)

        return graph
