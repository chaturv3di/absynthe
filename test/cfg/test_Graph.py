import unittest
import os

from absynthe.cfg import Graph, UniformNode


class GraphTest(unittest.TestCase):

    def test_basicErrors(self):
        graph = Graph("EmptyGraph", 0)
        uselessNode = UniformNode("UselessNode")

        # Node cannot be added since 'graph' is created
        # with numRoots = 0
        with self.assertRaises(IndexError):
            graph.addRoot(uselessNode)
        return

    def test_graphSizeZero(self):
        graph = Graph("EmptyGraph", 0)
        self.assertEqual(graph.size(), 0)
        return

    def _buildDummyGraph(self) -> Graph:
        root1 = UniformNode("Root1")
        nodeR1S1 = UniformNode("Root1_Succ1")
        nodeR1S2 = UniformNode("Root1_Succ2")
        root1.addSuccessor(nodeR1S1)
        root1.addSuccessor(nodeR1S2)

        # Add successors to nodeR1S1
        nodeS1S1 = UniformNode("Succ1_Succ1")
        nodeS1S2 = UniformNode("Succ1_Succ2")
        nodeR1S1.addSuccessor(nodeS1S1)
        nodeR1S1.addSuccessor(nodeS1S2)

        root2 = UniformNode("Root2")
        nodeR2S1 = UniformNode("Root2_Succ1")
        nodeR2S2 = UniformNode("Root2_Succ2")
        root2.addSuccessor(nodeR2S1)
        root2.addSuccessor(nodeR2S2)

        # Create a cycle with edge nodeR1S1 -> root1
        nodeR1S1.addSuccessor(root1)

        graph = Graph("TestGraph", 2)
        graph.addRoot(root1)
        graph.addRoot(root2)

        return graph

    def test_graphSizeNonZero(self):
        testGraph = self._buildDummyGraph()
        self.assertEqual(testGraph.size(), 8)
        return

    def test_graphDump(self):
        filePath = os.path.dirname("../resources")+"/Graph_test_graphDump.gv"
        testGraph = self._buildDummyGraph()
        with open(filePath, "w") as ofp:
            testGraph.dumpDotFile(ofp)
        return


if __name__ == '__main__':
    unittest.main()
