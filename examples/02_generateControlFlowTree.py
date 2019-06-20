import sys
import argparse

from absynthe.graph_builder import TreeBuilder


def treeGeneration(numRoots: int = 2, numLeaves: int = 4,
                   branching: int = 2, numInnerNodes: int = 16):
    loggerNodeTypes: str = "SimpleLoggerNode"
    tree_kwargs = {TreeBuilder.KW_NUM_ROOTS: str(numRoots),
                   TreeBuilder.KW_NUM_LEAVES: str(numLeaves),
                   TreeBuilder.KW_BRANCHING_DEGREE: str(branching),
                   TreeBuilder.KW_NUM_INNER_NODES: str(numInnerNodes),
                   TreeBuilder.KW_SUPPORTED_NODE_TYPES: loggerNodeTypes}

    simpleTreeBuilder = TreeBuilder(**tree_kwargs)
    simpleTreeBuilder.generateNewGraph().dumpDotFile(sys.stdout)
    return


if "__main__" == __name__:
    """
    Dumps a simple, tree-like control flow graph on standard output. This output can be redirected
    to a file and converted to an image using graphviz's 'dot' utility. The graph is generated with
    fair amount of randomness, so repeated invocations with the same set of parameters will yield
    different graphs.
    """
    argParser = argparse.ArgumentParser(description="Dumps a simple control flow graph on standard"
                                        + " output. This output can be redirected to a file and"
                                        + " converted to an image using graphviz's 'dot' utility."
                                        + " The graph is generated with fair amount of randomness,"
                                        + " so repeated invocations with identical parameters will"
                                        + " yield different graphs.")
    argParser.add_argument("-r", "--num_roots", required=True, type=int,
                           help="Number of roots in the graph.")
    argParser.add_argument("-l", "--num_leaves", type=int, required=True,
                           help="Number of leaves in the graph.")
    argParser.add_argument("-n", "--num_nodes", type=int, required=True,
                           help="Approximate number of inner nodes that this graph should contain."
                           + " The actual number is usually larger"
                           + " than what is specified here.")
    argParser.add_argument("-b", "--branching", type=int, required=True,
                           help="Approximate avg. branching degree of nodes in this graph.")
    args = argParser.parse_args()

    r: int = args.num_roots
    l: int = args.num_leaves
    n: int = args.num_nodes
    b: int = args.branching
    treeGeneration(r, l, b, n)
