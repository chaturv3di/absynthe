import unittest

from absynthe import TreeBuilder
from absynthe.cfg import Graph
import os


class TreeBuilderTest(unittest.TestCase):

    def test_basicTest(self):
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


if __name__ == '__main__':
    unittest.main()
