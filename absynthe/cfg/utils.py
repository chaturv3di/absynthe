from __future__ import print_function
from abc import ABC
from typing import List
from random import randint
from importlib import import_module

from absynthe.cfg import BinomialNode
from absynthe.cfg import LoggerNode


class Utils(ABC):
    """
    Utility methods for Nodes
    """

    # Node module
    LOGGER_NODE_MODULE = import_module("absynthe.cfg.logger_node")

    @staticmethod
    def generateID(entityType: str, entityNum: int) -> str:
        """
        Generates entity IDs from entity type and entity number.
        Args:
          entityType - Type of entity, e.g. "node", "leaf", "graph", etc.
          entityNum - Some number that uniquely identifies the entity.
        Returns:
          str - "entityType::entityNum"
        """
        return "::".join([entityType, str(entityNum)])

    @staticmethod
    def newRandomNode(nodeID: str,
                      loggerNodeOptions: List[str],
                      coreNodeOptions: List[str]) -> LoggerNode:
        """
        Instantiates an object of one of the concrete Node classes, wraps it
        inside one of the concrete LoggerNode classes, and returns the
        LoggerNode object.
        Args:
          nodeID - Identifier for the new node
          loggerNodeOptions - List of names of the possible, concrete
                              LoggerNode classes from which the return type
                              could be drawn
          coreNodeOptions - List of names of the possible, concrete Node
                            classes from which the core node of the above
                            LoggerNode could be drawn
        Returns:
          LoggerNode - A logger node
        """
        loggerNodeClassName = loggerNodeOptions[randint(0, len(loggerNodeOptions) - 1)]
        coreNodeClassName = coreNodeOptions[randint(0, len(coreNodeOptions) - 1)]
        logger_kwargs = {LoggerNode.KW_CORE_CLASS_NAME: coreNodeClassName,
                         LoggerNode.KW_IGNORE_PARAMS: "False"}

        if BinomialNode.__name__ == coreNodeClassName:
            logger_kwargs[BinomialNode.KW_P_VALUE] = "0.5"
        return getattr(Utils.LOGGER_NODE_MODULE, loggerNodeClassName)(nodeID, **logger_kwargs)
