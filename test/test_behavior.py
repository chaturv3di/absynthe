import unittest
import os

from absynthe.graph_builder import TreeBuilder, DCGBuilder
from absynthe.behavior import MonospaceInterleaving


class test_monospaceInterleaving(unittest.TestCase):

    def test_treeLogGeneration(self):
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
                                   "/test/resources/") + "/Tree_MonospaceInterleaving_test.log"
        with open(fileName, 'w') as logfile:
            for logLine in testBehavior.synthesize(2):
                logfile.write(logLine)
                logfile.write(os.linesep)

        return

    def test_DCGLogGeneration(self):
        dcg_kwargs = {DCGBuilder.KW_NUM_ROOTS: "2",
                      DCGBuilder.KW_NUM_LEAVES: "1",
                      DCGBuilder.KW_BRANCHING_DEGREE: "2",
                      DCGBuilder.KW_NUM_INNER_NODES: "16",
                      DCGBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        simpleDCGBuilder = DCGBuilder(**dcg_kwargs)

        wSessionID: bool = True
        testBehavior = MonospaceInterleaving(wSessionID)
        testBehavior.addGraph(simpleDCGBuilder.generateNewGraph())
        testBehavior.addGraph(simpleDCGBuilder.generateNewGraph())
        testBehavior.addGraph(simpleDCGBuilder.generateNewGraph())
        testBehavior.addGraph(simpleDCGBuilder.generateNewGraph())

        fileName = os.path.dirname(os.getcwd() +
                                   "/test/resources/") + "/DCG_MonospaceInterleaving_test.log"
        with open(fileName, 'w') as logfile:
            for logLine in testBehavior.synthesize(2):
                logfile.write(logLine)
                logfile.write(os.linesep)

        return
