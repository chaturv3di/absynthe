from __future__ import print_function
from sys import stderr
from typing import TextIO, List, Tuple

from .node import Node
from random import randint


class Graph(object):
    """
    The Graph class. Can have multiple root nodes; and it suffices
    for objects of this class to only keep track of the root nodes.

    The actual graph is defined by recursively following the
    successors of all the roots.

    NOTE: The nodes in the graph must all have unique IDs, otherwise
          it will result in unintended behaviour. For instance, the
          size() method will not work properly since it relies on
          unique IDs to count the number of nodes.
    """

    def __init__(self, id: str, numRoots: int = 1) -> None:
        """
        Constructor for the class.

        Args:
          id(str): A unique ID for the graph
          numRoots(int): The number of roots that this graph contains.
        """
        self._id = id
        self._numRoots = numRoots
        self._roots = []
        return

    def addRoot(self, root: Node):
        """
        Adds a root to this graph.
        Args:
          root(Node): A Node object to be added to the list of roots.
        Raises:
          IndexError: In case the list of roots already contains
                      _numRoots nodes in it.
        """
        if (len(self._roots) == self._numRoots):
            raise IndexError("Cannot accommodate any more root nodes.")

        self._roots.append(root)
        return

    def getRootAt(self, index: int = 0) -> Node:
        """
        Args:
          index(int): The index of the desired root, mindful of the order
                    in which roots were added to this graph.
        Returns:
          Node: The root at the given index.
        Raises:
          IndexError: If the index is out of bounds.
        """
        try:
            return self._roots[index]
        except IndexError as error:
            print("Illegal argument for index:", index,
                  "Number of root nodes:", len(self._roots),
                  "Expected number of root nodes:", self._numRoots,
                  file=stderr)
            raise error
        return None

    def getRootAtRandom(self) -> Node:
        """
        Returns:
          Node: One of the root nodes of this graph, selecte uniformly
                at random.
        """
        randomIndex = randint(0, len(self._roots) - 1)
        return self._roots[randomIndex]

    def getID(self) -> str:
        return self._id

    def _bfsAndCount(self, node: Node) -> int:
        """
        Search the tree located below 'node' in a breadth-first manner,
        and return the count of this sub-tree, incl. 'node'in the count.

        Args:
          node(Node): The node, the size of whose sub-tree is to be
                      computed.
        Returns:
          int: The number of nodes in the sub-tree rooted at 'node',
               including 'node'.
        """
        nodeID = node.getID()
        try:
            _ = self._nodeDict[nodeID]
            return 0
        except KeyError:
            self._nodeDict[nodeID] = True
            pass
        count = 1

        for i in range(node.getNumSuccessors()):
            count += self._bfsAndCount(node.getSuccessorAt(i))
        return count

    def size(self) -> int:
        """
        Returns:
          int: The total number of nodes (with unique IDs) in this graph.
               If there are multiple Node objects with identical IDs,
               then this method will not produce expected result.
        """
        size = 0
        self._nodeDict = dict()
        for r in self._roots:
            if r is not None:
                size += self._bfsAndCount(r)
        return size

    def _bfsAndAdd(self, node: Node, transitionList: List[Tuple[str, str]]) -> None:
        nodeID = node.getID()
        try:
            _ = self._nodeDict[nodeID]
            return
        except KeyError:
            self._nodeDict[nodeID] = True
            pass

        for i in range(node.getNumSuccessors()):
            succNode: Node = node.getSuccessorAt(i)
            succNodeID = succNode.getID()
            transitionList.append((nodeID, succNodeID))
            self._bfsAndAdd(succNode, transitionList)

        return

    def dumpDotFile(self, fp: TextIO) -> None:
        """
        Creates a file that could be visualised using graphviz's DOT program.
        Args:
          fp(typing.TextIO): A text file stream that can be written to.
        """
        self._nodeDict = dict()
        transitionList: List[Tuple[str, str]] = list()

        for r in self._roots:
            if r is not None:
                self._bfsAndAdd(r, transitionList)

        fileContent: List[str] = ["digraph \""]
        fileContent.append(self._id)
        fileContent.append("\" {\n")

        for transition in transitionList:
            fileContent.append("\t\"")
            fileContent.append(transition[0])
            fileContent.append("\" -> \"")
            fileContent.append(transition[1])
            fileContent.append("\";\n")

        fileContent.append("}\n")

        fileText = "".join(fileContent)
        fp.write(fileText)
        fp.flush()
        return
