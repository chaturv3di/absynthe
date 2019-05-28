import unittest

from absynthe.graph_builder import TreeBuilder
from absynthe.behaviors import SimpleBehavior


class test_simpleBehavior(unittest.TestCase):
    tree_kwargs = {TreeBuilder.KW_NUM_ROOTS: "2",
                   TreeBuilder.KW_NUM_LEAVES: "4",
                   TreeBuilder.KW_BRANCHING_DEGREE: "2",
                   TreeBuilder.KW_MIN_NUM_INNER_NODES: "8",
                   TreeBuilder.KW_MAX_NUM_INNER_NODES: "16",
                   TreeBuilder.KW_SUPPORTED_NODE_TYPES: "SimpleLoggerNode"}

    simpleTreeBuilder = TreeBuilder(**tree_kwargs)

    testBehavior = SimpleBehavior()
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())

    for logLine in testBehavior.synthesize(2):
        print(logLine)
