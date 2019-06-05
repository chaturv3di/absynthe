import unittest
import os

from absynthe import TreeBuilder, MonospaceInterleaving


class test_monospaceInterleaving(unittest.TestCase):

    def test_basicLogGeneration(self):
        tree_kwargs = {TreeBuilder.KW_NUM_ROOTS: "2",
                       TreeBuilder.KW_NUM_LEAVES: "4",
                       TreeBuilder.KW_BRANCHING_DEGREE: "2",
                       TreeBuilder.KW_NUM_INNER_NODES: "16",
                       TreeBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        simpleTreeBuilder = TreeBuilder(**tree_kwargs)

        wSessionID: bool = True
        testBehavior = MonospaceInterleaving(wSessionID)
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
        testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())

        fileName = os.path.dirname(os.getcwd() +
                                   "/test/resources/") + "/MonospaceInterleaving_test.log"
        with open(fileName, 'w') as logfile:
            for logLine in testBehavior.synthesize(2):
                logfile.write(logLine)
                logfile.write(os.linesep)
