import unittest
import os

from absynthe.graph_builder import TreeBuilder
from absynthe.behaviors import SimpleBehavior


class test_simpleBehavior(unittest.TestCase):

    def test_basicLogGeneration(self):
        tree_kwargs = {TreeBuilder.KW_NUM_ROOTS: "2",
                       TreeBuilder.KW_NUM_LEAVES: "4",
                       TreeBuilder.KW_BRANCHING_DEGREE: "2",
                       TreeBuilder.KW_MIN_NUM_INNER_NODES: "8",
                       TreeBuilder.KW_MAX_NUM_INNER_NODES: "16",
                       TreeBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        simpleTreeBuilder = TreeBuilder(**tree_kwargs)

        wSessionID: bool = True
        testBehavior = SimpleBehavior(wSessionID)
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())

        fileName = os.path.dirname(os.getcwd() + "/test/resources/") + "/SimpleBehavior_test.log"
        with open(fileName, 'w') as logfile:
            for logLine in testBehavior.synthesize(2):
                logfile.write(logLine)
                logfile.write(os.linesep)
