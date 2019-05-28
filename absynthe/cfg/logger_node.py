from __future__ import print_function

# Imports for LoggerNode
from .node import Node

from abc import abstractmethod
from sys import stderr
from typing import List
from random import randint
from importlib import import_module


class LoggerNode(Node):
    """
    An abstract wrapper class that provides the additional functionality of
    generating actual log messages. This class has a member field _coreNode
    that is a concrete subclass of Node, which ought to be available from
    importing absynthe.cfg.node.<ConcreteClassName>.

    This class is also a subclass of Node, and it implements all of the
    abstract methods of Node by delegating the call to _coreNode. This
    class additionally specifies methods to spit out actual, non-trivial,
    log messages.
    """

    # Keys expected in the kwargs parameter provided to the constructor
    # of this class.

    # To specify the class of the core node
    KW_CORE_CLASS_NAME = "CORE_CLASS_NAME"

    # Some nodes ignore flow params while spitting out the log message.
    KW_IGNORE_PARAMS = "IGNORE_PARAMS"

    # Type of messages supported
    MESG_TYPE_INFO = "INFO"
    MESG_TYPE_ERR = "ERROR"

    def __init__(self, id: str, **kwargs: str) -> None:
        """
        Constructor that internally creates an object of a concrete
        subclass of Node and assigns it to the member field _coreNode. The
        name of the concrete subclass is obtained through the keyword
        arguments, using the key 'coreClassName'.
        Args:
          id(str): Unique identifier for this node
          **kwargs(str): A dictionary of str -> str specifying, among
                         other things, the type of core node wrapped
                         inside this object. Must contain a key-value pair
                         against the key 'coreClassName' where the value is
                         the name of a concrete subclass of Node.

                         This argument is passed as is to the super class
                         constructor, as well as to the constructor of the
                         core node class. So it can contain keywords
                         specific to those constructors.
        Raises:
          AttributeError: If the value provided for 'coreClassName' is not a
                          valid class defined in absynthe.cfg.node module.
          TypeError: If the value provided for 'coreClassName' is a class
                     that cannot be instantiated, e.g. an abstract class.
        """
        super().__init__(id, **kwargs)
        coreID = id + "_Core"
        nodeModule = import_module("absynthe.cfg.node")

        # 1. Try to initialise the core node of this object
        self._coreNode: Node = None
        try:
            className = kwargs[LoggerNode.KW_CORE_CLASS_NAME]
            self._coreNode = getattr(nodeModule, className)(coreID, **kwargs)
        except KeyError as ke:
            # A core class name is mandatory...
            print(type(self).__name__, "ERROR: Keyword LoggerNode.KW_CORE_CLASS_NAME not provided",
                  className, file=stderr)
            raise ke
        except AttributeError as ae:
            # ...and shoud be a subclass of Node,
            print(type(self).__name__, "ERROR: Not a valid concrete subclass of Node - ",
                  className, file=stderr)
            raise ae
        except TypeError as te:
            # and should not be an abstract class.
            print(type(self).__name__, "ERROR: Class cannot be instantiated - ",
                  className, file=stderr)
            raise te

        # 2. Set other params used by methods that print out log messages
        self._ignoreParams = False
        try:
            ignoreParams = kwargs[LoggerNode.KW_IGNORE_PARAMS].lower()
            self._ignoreParams = (ignoreParams == "true")
        except KeyError:
            pass

        return

    def printDebugInfo(self, verbose: bool = False, printPrefix: str = "") -> None:
        """
        Override method to just print this node's ID ahead of the
        remainder of debug info that is generated from core ndoe.
        """
        print(printPrefix, self._id)
        self._coreNode.printDebugInfo(verbose, printPrefix)
        return

    def addSuccessor(self, successor: Node):
        """
        Override abstract method by delegating to core node.
        """
        self._coreNode.addSuccessor(successor)
        return

    def delLastSuccessor(self) -> Node:
        """
        Override abstract method by delegating to core node.
        """
        return self._coreNode.delLastSuccessor()

    def getNumSuccessors(self) -> int:
        """
        Override abstract method by delegating to core node.
        """
        return self._coreNode.getNumSuccessors()

    def getSuccessorAt(self, index: int) -> Node:
        """
        Override abstract method by delegating to core node.
        """
        return self._coreNode.getSuccessorAt(index)

    def getSuccessorAtRandom(self) -> Node:
        """
        Override abstract method by delegating to core node.
        """
        return self._coreNode.getSuccessorAtRandom()

    @abstractmethod
    def logInfo(self, timeStamp: str, params: List[str]) -> str:
        """
        Create a log message comprising of some fixed part and some variable part.
        The fixed part (i.e. the subseqeuence defining the log signature) ought to
        be immutable through the life of this object.

        The instantaneous parameter (e.g. the function call argument) is provided
        by the 'params' argument. This argument ought to be ignored if the field
        _ignoreParams is 'True'.
        Args:
          timeStamp(str): The time stamp associated with this log line
          params(List[str]): All the parameters that describe the variable part.
        Returns:
          str: A log message that respects _ignoreParams.
        """
        pass

    @abstractmethod
    def logError(self, timeStamp: str, params: List[str]) -> str:
        """
        Create an error message comprising of some fixed part and some variable part.
        The fixed part (i.e. the subseqeuence defining the log signature) ought to be
        immutable through the life of this object.

        The instantaneous parameter (e.g. the function call argument) is provided
        by the 'params' argument. This argument ought to be ignored if the field
        _ignoreParams is 'True'.
        Args:
          timeStamp(str): The time stamp associated with this log line
          params(List[str]): All the parameters that describe the variable part.
        Returns:
          str: A log message that respects _ignoreParams.
        """
        pass


class SimpleLoggerNode(LoggerNode):

    MIN_MESG_SIZE = 1
    MAX_MESG_SIZE = 4

    KW_PREFIX = "PREFIX"

    def __init__(self, id: str, **kwargs: str) -> None:
        super().__init__(id, **kwargs)
        meta: str = None
        try:
            meta = kwargs[SimpleLoggerNode.KW_PREFIX]
        except KeyError:
            pass
        except TypeError as te:
            print(type(self).__name__,
                  "ERROR: Expect keyword KW_PREFIX to provide `str` type.",
                  file=stderr)
            raise te
        prefix = meta if meta else ""
        self._fixedInfoMesg = self._createLoglineSignature(id, prefix)
        prefix += " ERROR"
        self._fixedErrMesg = self._createLoglineSignature(id, prefix)
        return

    def _createLoglineSignature(self, id: str, mesgPrefix: str = "") -> str:
        """
        Create and store a fixed signature that would be emitted with every log
        message. This node has different fixed signatures for info and error.
        """
        self._mesgLen = randint(self.MIN_MESG_SIZE, self.MAX_MESG_SIZE)
        fixedMesgList = [mesgPrefix]

        mesgInfixes = [self._id, self._coreNode.getID()]
        mesgInfix = mesgPrefix + "-" if not mesgPrefix == "" else None
        for i in range(self._mesgLen):
            fixedMesgList.append(" ")
            if mesgInfix:
                fixedMesgList.append(mesgInfix)
            for j in range(i + 1):
                fixedMesgList.append(mesgInfixes[j % 2])
                fixedMesgList.append("::")
            _ = fixedMesgList.pop()

        return "".join(fixedMesgList)

    def logInfo(self, timeStamp: str, params: List[str]) -> str:
        """
        Override abstract method of super class
        """
        return self._createMesg(timeStamp, params, LoggerNode.MESG_TYPE_INFO)

    def logError(self, timeStamp: str, params: List[str]) -> str:
        """
        Override abstract method of super class
        """
        return self._createMesg(timeStamp, params, LoggerNode.MESG_TYPE_ERR)

    def _createMesg(self, timeStamp: str,
                    params: List[str],
                    mesgType: str = LoggerNode.MESG_TYPE_INFO) -> str:
        mesgList = list()
        if mesgType == LoggerNode.MESG_TYPE_INFO:
            mesgList = [timeStamp, " ", self._fixedInfoMesg]
        elif mesgType == LoggerNode.MESG_TYPE_ERR:
            mesgList = [timeStamp, " ", self._fixedErrMesg]
        else:
            raise ValueError(type(self).__name__,
                             " ERROR: Unsupported type of log message -- ",
                             mesgType)

        if params is not None and not self._ignoreParams:
            mesgList.append(" [WITH_PARAMS] ")
            mesgList.extend(params)

        return "".join(mesgList)
