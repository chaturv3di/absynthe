import unittest
import os

from absynthe.graph_builder import TreeBuilder, DCGBuilder
from absynthe.behavior import MonospaceSimple, MonospaceInterleaving


class test_monospaceSimple(unittest.TestCase):

    def test_DCGLogGeneration(self):
        dcg_kwargs = {DCGBuilder.KW_NUM_ROOTS: "2",
                      DCGBuilder.KW_NUM_LEAVES: "1",
                      DCGBuilder.KW_BRANCHING_DEGREE: "2",
                      DCGBuilder.KW_NUM_INNER_NODES: "16",
                      DCGBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        simpleDCGBuilder = DCGBuilder(**dcg_kwargs)

        testBehavior = MonospaceSimple()
        for _ in range(4):
            testBehavior.addGraph(simpleDCGBuilder.generateNewGraph())

        wSessionID: bool = False
        fileName = os.path.dirname(os.getcwd() +
                                   "/test/resources/") + "/DCG_MonospaceSimple_test.log"
        with open(fileName, 'w') as logfile:
            for logLine in testBehavior.synthesize(2, wSessionID):
                logfile.write(logLine)
                logfile.write(os.linesep)

            # Now generate logs with session IDs, using the same graphs
            wSessionID = True
            logfile.write("===========\n===========\n\n")
            for logLine in testBehavior.synthesize(2, wSessionID):
                logfile.write(logLine)
                logfile.write(os.linesep)

        return


class test_monospaceInterleaving(unittest.TestCase):

    def test_treeLogGeneration(self):
        tree_kwargs = {TreeBuilder.KW_NUM_ROOTS: "2",
                       TreeBuilder.KW_NUM_LEAVES: "4",
                       TreeBuilder.KW_BRANCHING_DEGREE: "2",
                       TreeBuilder.KW_NUM_INNER_NODES: "16",
                       TreeBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        simpleTreeBuilder = TreeBuilder(**tree_kwargs)

        testBehavior = MonospaceInterleaving()
        for _ in range(4):
            testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())

        wSessionID: bool = True
        fileName = os.path.dirname(os.getcwd() +
                                   "/test/resources/") + "/Tree_MonospaceInterleaving_test.log"
        with open(fileName, 'w') as logfile:
            for logLine in testBehavior.synthesize(2, wSessionID):
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

        testBehavior = MonospaceInterleaving()
        for _ in range(4):
            testBehavior.addGraph(simpleDCGBuilder.generateNewGraph())

        wSessionID: bool = False
        fileName = os.path.dirname(os.getcwd() +
                                   "/test/resources/") + "/DCG_MonospaceInterleaving_test.log"
        with open(fileName, 'w') as logfile:
            for logLine in testBehavior.synthesize(2, wSessionID):
                logfile.write(logLine)
                logfile.write(os.linesep)

        return
