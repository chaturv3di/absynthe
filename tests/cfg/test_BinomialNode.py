import unittest
from scipy.stats import binom

from absynthe.cfg import BinomialNode
from collections import defaultdict


class BinomialNodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        node_kwargs = {BinomialNode.KW_P_VALUE: "0.5"}
        self.BinomialNode = BinomialNode("Test_Node", **node_kwargs)
        succ1 = BinomialNode("Successor_1", **node_kwargs)
        succ2 = BinomialNode("Successor_2", **node_kwargs)
        succ3 = BinomialNode("Successor_3", **node_kwargs)
        self.BinomialNode.addSuccessor(succ1)
        self.BinomialNode.addSuccessor(succ2)
        self.BinomialNode.addSuccessor(succ3)
        # self.BinomialNode.printDebugInfo(True)
        return

    def test_01_numSuccessors(self):
        self.assertEqual(self.BinomialNode.getNumSuccessors(), 3)
        return

    def helper_diffWithinTolerance(self, val1: int, val2: int, tolerance: int = 150) -> bool:
        return (abs(val1 - val2) <= tolerance)

    def test_02_binomialDistribution(self):
        numSucc = self.BinomialNode.getNumSuccessors()
        totalCount = numSucc * 5000

        succCount = defaultdict(int)
        expectedIndividualCounts = [totalCount * binom.pmf(k, numSucc - 1, self.BinomialNode._p) for k in range(numSucc)]
        for _ in range(totalCount):
            succName = self.BinomialNode.getSuccessorAtRandom().getID()
            succCount[succName] += 1

        # all individual counts must be within 5% of expectedIndividualCount
        tolerances = [(count * 5) // 100 for count in expectedIndividualCounts]
        for i in range(numSucc):
            id = self.BinomialNode.getSuccessorAt(i).getID()
            count = succCount[id]
            self.assertTrue(self.helper_diffWithinTolerance(count,
                                                            expectedIndividualCounts[i],
                                                            tolerances[i]))

    def test_03_deleteSuccessor(self):
        originalNumSuccessors = self.BinomialNode.getNumSuccessors()
        expectedSucc3 = self.BinomialNode.getSuccessorAt(-1)
        actualSucc3 = self.BinomialNode.delLastSuccessor()
        newNumSuccessors = self.BinomialNode.getNumSuccessors()

        self.assertEqual(expectedSucc3.getID(), actualSucc3.getID())
        self.assertEqual(originalNumSuccessors, newNumSuccessors + 1)

    def test_04_noSuccessors_pt1(self):
        node_kwargs = {BinomialNode.KW_P_VALUE: "0.5"}
        testNode = BinomialNode("testNode", **node_kwargs)
        self.assertEqual(testNode.getSuccessorAtRandom(), None)

    def test_04_noSuccessors_raises_IndexError(self):
        node_kwargs = {BinomialNode.KW_P_VALUE: "0.5"}
        testNode = BinomialNode("testNode", **node_kwargs)
        with self.assertRaises(IndexError):
            testNode.getSuccessorAt(0)


if __name__ == '__main__':
    unittest.main()
