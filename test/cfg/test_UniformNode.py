import unittest

from absynthe.cfg import UniformNode
from collections import defaultdict


class UniformNodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.UniformNode = UniformNode("Test_Node")
        succ1 = UniformNode("Successor_1")
        succ2 = UniformNode("Successor_2")
        succ3 = UniformNode("Successor_3")
        self.UniformNode.addSuccessor(succ1)
        self.UniformNode.addSuccessor(succ2)
        self.UniformNode.addSuccessor(succ3)
        # self.UniformNode.printDebugInfo(True)
        return

    def test_01_numSuccessors(self):
        self.assertEqual(self.UniformNode.getNumSuccessors(), 3)
        return

    def helper_diffWithinTolerance(self, val1: int, val2: int, tolerance: int = 150) -> bool:
        return (abs(val1 - val2) <= tolerance)

    def test_02_uniformDistribution(self):
        numSucc = self.UniformNode.getNumSuccessors()

        succCount = defaultdict(int)
        expectedIndividualCount = 5000
        for _ in range(numSucc * expectedIndividualCount):
            succName = self.UniformNode.getSuccessorAtRandom().getID()
            succCount[succName] += 1

        # all individual counts must be within 5% of expectedIndividualCount
        tolerance = (expectedIndividualCount * 5) // 100
        for i in range(numSucc):
            id = self.UniformNode.getSuccessorAt(i).getID()
            count = succCount[id]
            self.assertTrue(self.helper_diffWithinTolerance(count,
                                                            expectedIndividualCount,
                                                            tolerance))

    def test_03_deleteSuccessor(self):
        originalNumSuccessors = self.UniformNode.getNumSuccessors()
        expectedSucc3 = self.UniformNode.getSuccessorAt(-1)
        actualSucc3 = self.UniformNode.delLastSuccessor()
        newNumSuccessors = self.UniformNode.getNumSuccessors()

        self.assertEqual(expectedSucc3.getID(), actualSucc3.getID())
        self.assertEqual(originalNumSuccessors, newNumSuccessors + 1)

    def test_04_noSuccessors_pt1(self):
        testNode = UniformNode("testNode")
        self.assertEqual(testNode.getSuccessorAtRandom(), None)

    def test_04_noSuccessors_raises_IndexError(self):
        testNode = UniformNode("testNode")
        with self.assertRaises(IndexError):
            testNode.getSuccessorAt(0)


if __name__ == '__main__':
    unittest.main()
