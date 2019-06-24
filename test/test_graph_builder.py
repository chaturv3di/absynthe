import unittest

from absynthe.graph_builder import TreeBuilder, DAGBuilder, DCGBuilder
from absynthe.cfg import Graph
import os


class TreeBuilderTest(unittest.TestCase):

    def test_treeTest(self):
        tree_kwargs = {TreeBuilder.KW_NUM_ROOTS: "2",
                       TreeBuilder.KW_NUM_LEAVES: "4",
                       TreeBuilder.KW_BRANCHING_DEGREE: "2",
                       TreeBuilder.KW_NUM_INNER_NODES: "16",
                       TreeBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        testTreeBuilder = TreeBuilder(**tree_kwargs)
        testTree: Graph = testTreeBuilder.generateNewGraph()
        fileName = os.path.dirname(os.getcwd()
                                   + "/test/resources/") + "/TreeBuilder_test_TreeDump.gv"
        with open(fileName, 'w') as f:
            testTree.dumpDotFile(f)
        return

    def test_DAGTest(self):
        cfg_kwargs = {DAGBuilder.KW_NUM_ROOTS: "2",
                      DAGBuilder.KW_NUM_LEAVES: "4",
                      DAGBuilder.KW_BRANCHING_DEGREE: "3",
                      DAGBuilder.KW_NUM_INNER_NODES: "32",
                      DAGBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        testDAGBuilder = DAGBuilder(**cfg_kwargs)
        testDAG: Graph = testDAGBuilder.generateNewGraph()
        fileName = os.path.dirname(os.getcwd()
                                   + "/test/resources/") + "/DAGBuilder_test_DAGDump.gv"
        with open(fileName, 'w') as f:
            testDAG.dumpDotFile(f)
        return

    def test_DCGTest(self):
        cfg_kwargs = {DCGBuilder.KW_NUM_ROOTS: "2",
                      DCGBuilder.KW_NUM_LEAVES: "4",
                      DCGBuilder.KW_BRANCHING_DEGREE: "3",
                      DCGBuilder.KW_NUM_INNER_NODES: "32",
                      DCGBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

        testDCGBuilder = DCGBuilder(**cfg_kwargs)
        testDCG: Graph = testDCGBuilder.generateNewGraph()
        fileName = os.path.dirname(os.getcwd()
                                   + "/test/resources/") + "/DCGBuilder_test_DCGDump.gv"
        with open(fileName, 'w') as f:
            testDCG.dumpDotFile(f)
        return


if __name__ == '__main__':
    unittest.main()
