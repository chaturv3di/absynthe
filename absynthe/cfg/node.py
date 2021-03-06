from __future__ import print_function
from sys import stderr

# Imports for Node
from abc import ABC, abstractmethod

# Imports for UniformNode
from random import randint

# Import for BinomialNode
from scipy.stats import binom
from random import random


class Node(ABC):
    """
    Abstract base class for nodes in a CFG. Each node would describe
    its own branching method based on the probability distribution
    governing the choice of which successor to return for traversal.
    """

    def __init__(self, id: str, **kwargs: str) -> None:
        """
        Args:
          id(str): An identifier for this node. It would help to
                   ensure that it is unique for a given use case.
          **kwargs(str): Keyword arguments specifying, among other
                   things, the probability mass function over the
                   choice of successors.
        """
        self._id = id
        self._successors = list()
        return

    # Concrete methods

    def getID(self) -> str:
        """
        Returns:
          str: The identifier for this node.
        """
        return self._id

    def getNumSuccessors(self) -> int:
        """
        Returns:
          int: Number of successors of this node.
        """
        return len(self._successors)

    def printDebugInfo(self, verbose: bool = False, printPrefix: str = "") -> None:
        """
        Prints information about this node. This must at least include
        the id and number of successors.
        Args:
          verbose(bool): If true, then the debug information ought to
                         contain debug information of the successors too.
        """
        print(printPrefix, self._id, "\b:", type(self).__name__)
        printPrefix += "\t"
        print(printPrefix, "Num Successors:", self.getNumSuccessors())

        for i in range(self.getNumSuccessors()):
            successor = self.getSuccessorAt(i)
            if verbose:
                successor.printDebugInfo(printPrefix=printPrefix)
            else:
                print(printPrefix, successor.getID())
        return

    # Abstract methods

    @abstractmethod
    def addSuccessor(self, successor: object) -> None:
        """
        Appends a successor Node to the list of successors. The
        order of successors is important since it governs the
        return value of delLastSuccessor() method.

        Additionally, it *might* govern the probability of selecting
        a successor if, e.g., the selection is made using a Gaussian
        distribution. In particular, the successor Nodes toward the
        centre of the list of successors would have the maximum
        probability of selection in that case.

        Args:
          successor(Node): A successor node to be added. `None` is a valid
            successor, since it denotes that this node could be a leaf node.
            Note that a node can have both `None` and non-`None` successors.
        """
        pass

    @abstractmethod
    def delLastSuccessor(self) -> object:
        """
        Delete the last successor that was added using the
        addSuccessor() method.
        """
        pass

    @abstractmethod
    def getSuccessorAt(self, index: int) -> object:
        """
        If the successors of this node are stored in an ordered list or,
        equivalently, uniquely mapped to 0-indexed integers, then this
        method should return the successor by the index value.

        Args:
          index(int): The index of a successor node.
        Returns:
          Node: The successor node at the given index.
        Raises:
          IndexError: If the index is out of bounds. Typically, index
                      takes values from 0 to getNumSuccessors - 1.
        """
        try:
            return self._successors[index]
        except IndexError as error:
            print("Illegal argument for index:", index, file=stderr)
            raise error

    @abstractmethod
    def getSuccessorAtRandom(self) -> object:
        """
        This method captures the probability distribution that governs
        the choice of successors while a behaviour is being synthesized.
        """
        pass


# ##
# Below are some concrete implementations of Node.
# ##

class UniformNode(Node):
    """
    A concrete implementation of Node that selects its successors
    *uniformly at random*.
    """

    def __init__(self, id, **kwargs) -> None:
        super().__init__(id, **kwargs)
        return

    def addSuccessor(self, successor: Node) -> None:
        """
        Appends a successor Node to the list of successors. Ensures that
        *at most one* successor is `None`.
        """
        if successor is None:
            try:
                # Check if None is already a successor
                _ = self._successors.index(None)
                return
            except ValueError:
                # If not, then add it.
                pass
        self._successors.append(successor)
        return

    def delLastSuccessor(self) -> Node:
        """
        Returns:
          Node: The last successor node that was added via
                addSuccessor() method.
        """
        return self._successors.pop()

    def getSuccessorAt(self, index: int) -> Node:
        return super().getSuccessorAt(index)

    def getSuccessorAtRandom(self) -> Node:
        if 0 == self.getNumSuccessors():
            return None

        randomIndex = randint(0, self.getNumSuccessors() - 1)
        return self._successors[randomIndex]


class BinomialNode(Node):
    """
    A concrete implementation of Node class that chooses its successors
    using a binomial PMF. For example, if a BinomialNode, with the parameter
    'p' = 0.5, has three successors then it will choose them with
    probabilities 0.25, 0.5, and 0.25 respectively.

    The second parameter 'n' of the binomial distribution is set
    automatically from the number of successors that are ultimately assigned
    to a BinomialNode.
    """

    # Keywords for kwargs expected by the constructor
    KW_P_VALUE = "P_VALUE"

    def __init__(self, id, **kwargs) -> None:
        """
        Construtor for the class.
        Args:
          **kwargs(str): Must have the following keywords.
            KW_P - Specifying the parameter 'p' of the binomial distribution
        """
        super().__init__(id, **kwargs)

        self._p = 0.5
        try:
            self._p = float(kwargs[BinomialNode.KW_P_VALUE])
        except KeyError as ke:
            print(type(self).__name__,
                  "ERROR - Probability value must be specified using the key",
                  "BinomialNode.KW_P_VALUE", file=stderr)
            raise ke
        return

    def addSuccessor(self, successor: Node) -> None:
        if successor is None:
            try:
                # Check if None is already a successor
                _ = self._successors.index(None)
            except ValueError:
                # Add it...
                pass
        self._successors.append(successor)
        return

    def delLastSuccessor(self) -> Node:
        return self._successors.pop()

    def getSuccessorAt(self, index: int) -> Node:
        return super().getSuccessorAt(index)

    def getSuccessorAtRandom(self) -> Node:
        """
        Returns:
          Node - A successor Node chosen according to the binomial
                 distribution parameterized by (n, p), where 'n' is the
                 number of successors of this node, and 'p' is provided in
                 the constructor. The probability of selecting a successor
                 at position k is pmf(k, n - 1, p), where 0 <= k <= n - 1.
        """
        numSuccessors: int = self.getNumSuccessors()

        if 0 == numSuccessors:
            return None

        p: float = random()

        for idx in range(numSuccessors):
            if p <= binom.cdf(idx, numSuccessors - 1, self._p):
                return self._successors[idx]
