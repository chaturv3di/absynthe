from __future__ import print_function
from abc import ABC
from typing import List
from random import randint
from importlib import import_module

from absynthe.cfg import Node, BinomialNode
from absynthe.cfg import LoggerNode


class Utils(ABC):

    # Node module
    LOGGER_NODE_MODULE = import_module("absynthe.cfg.logger_node")

    @staticmethod
    def generateID(entityType: str, nodeNum: int) -> str:
        return "::".join([entityType, str(nodeNum)])

    @staticmethod
    def newRandomNode(eType: str, numNodes: int,
                      loggerNodeOptions: List[str],
                      coreNodeOptions: List[str]) -> Node:
        id = Utils.generateID(eType, numNodes)
        loggerNodeClassName = loggerNodeOptions[randint(0, len(loggerNodeOptions) - 1)]
        coreNodeClassName = coreNodeOptions[randint(0, len(coreNodeOptions) - 1)]
        logger_kwargs = {LoggerNode.KW_CORE_CLASS_NAME: coreNodeClassName,
                         LoggerNode.KW_IGNORE_PARAMS: "False"}

        if BinomialNode.__name__ == coreNodeClassName:
            logger_kwargs[BinomialNode.KW_P_VALUE] = "0.5"
        return getattr(Utils.LOGGER_NODE_MODULE, loggerNodeClassName)(id, **logger_kwargs)
