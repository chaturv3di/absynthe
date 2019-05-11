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


class GraphBuilder(ABC):
    """
    The abstract base class for all kinds of graph builders. Each graph builder object takes keyword arguments to
    initialise itself. The base class only specifies one method, `generateNewGraph()`, which should be able to
    generate a *new* graph with every invocation (subject to the initialising parameters).
    """

    KEY_NUM_ROOTS = "NUM_ROOTS"
    KEY_NUM_LEAVES = "NUM_LEAVES"
    KEY_MIN_NUM_INNER_NODES = "MIN_NUM_INNER_NODES"
    KEY_MAX_NUM_INNER_NODES = "MAX_NUM_INNER_NODES"
    KEY_BRANCHING_DEGREE = "BRANCHING_DEGREE"
    KEY_SUPPORTED_NODE_TYPES = "SUPPORTED_NODE_TYPES"

    def __init__(self, **kwargs: str) -> None:
        """
        """
        # Fields that would be initialised from user input.
        # Failure to initialise any one of these will raise an error.
        self._numRoots: int = 0
        self._numLeaves: int = 0
        self._minNumInnerNodes: int = 0
        self._maxNumInnerNodes: int = 0
        self._branchingDegree: int = 0
        self._supportedNodeTypes: List[str] = None

        try:
            self._numRoots = int(kwargs[GraphBuilder.KEY_NUM_ROOTS])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Number of roots must be specified using the key GraphBuilder.KEY_NUM_ROOTS.",
                  file=stderr)
            raise ke

        try:
            self._numLeaves = int(kwargs[GraphBuilder.KEY_NUM_LEAVES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Number of leaves must be specified using the key GraphBuilder.KEY_NUM_LEAVES.",
                  file=stderr)
            raise ke

        try:
            self._minNumInnerNodes = int(kwargs[GraphBuilder.KEY_MIN_NUM_INNER_NODES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Minimum number of inner nodes must be specified using the key GraphBuilder.KEY_MIN_NUM_INNER_NODES.",
                  file=stderr)
            raise ke

        try:
            self._maxNumInnerNodes = int(kwargs[GraphBuilder.KEY_MAX_NUM_INNER_NODES])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Maximum number of inner nodes must be specified using the key GraphBuilder.KEY_MAX_NUM_INNER_NODES.",
                  file=stderr)
            raise ke

        try:
            self._branchingDegree = int(kwargs[GraphBuilder.KEY_BRANCHING_DEGREE])
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Approx. branching degree must be specified using the key GraphBuilder.KEY_BRANCHING_DEGREE.",
                  file=stderr)
            raise ke

        try:
            self._supportedNodeTypes = [x.strip() for x in kwargs[GraphBuilder.KEY_SUPPORTED_NODE_TYPES]]
        except KeyError as ke:
            print(type(self).__name__,
                  " ERROR - Types of nodes supported in this graph must be specified using the key GraphBuilder.KEY_SUPPORTED_NODE_TYPES as comma-separated list of class names.",
                  file=stderr)
            raise ke

        # Everything okay, so instantiate object to 

        return

    @abstractmethod
    def generateNewGraph(self) -> Graph:
        pass
