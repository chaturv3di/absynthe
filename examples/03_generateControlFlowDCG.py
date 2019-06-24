import sys
import argparse

from absynthe.graph_builder import DCGBuilder


def dcgGeneration(numRoots: int = 2, numLeaves: int = 4,
                  branching: int = 2, numInnerNodes: int = 16,
                  reverseEdges: bool = False):
    loggerNodeTypes: str = "SimpleLoggerNode"
    dcg_kwargs = {DCGBuilder.KW_NUM_ROOTS: str(numRoots),
                  DCGBuilder.KW_NUM_LEAVES: str(numLeaves),
                  DCGBuilder.KW_BRANCHING_DEGREE: str(branching),
                  DCGBuilder.KW_NUM_INNER_NODES: str(numInnerNodes),
                  DCGBuilder.KW_SUPPORTED_NODE_TYPES: loggerNodeTypes,
                  DCGBuilder.KW_REVERSE_EDGES: reverseEdges}

    simpleDCGBuilder = DCGBuilder(**dcg_kwargs)
    simpleDCGBuilder.generateNewGraph().dumpDotFile(sys.stdout)
    return


if "__main__" == __name__:
    """
    Dumps a directed cyclic control flow graph on standard output. This output can be redirected to
    a file and converted to an image using graphviz's 'dot' utility. The graph is generated with
    fair amount of randomness, so repeated invocations with the same set of parameters will yield
    different graphs.
    """
    argParser = argparse.ArgumentParser(description="Dumps a simple control flow graph on standard"
                                        + " output. This output can be redirected to a file and"
                                        + " converted to an image using graphviz's 'dot' utility."
                                        + " The graph is generated with fair amount of randomness,"
                                        + " so repeated invocations with identical parameters will"
                                        + " yield different graphs.")
    argParser.add_argument("-r", "--num-roots", dest="num_roots", type=int, required=True,
                           help="Number of roots in the graph.")
    argParser.add_argument("-l", "--num-leaves", dest="num_leaves", type=int, required=True,
                           help="Number of leaves in the graph.")
    argParser.add_argument("-n", "--num-nodes", dest="num_nodes", type=int, required=True,
                           help="Approximate number of inner nodes that this graph should contain."
                           + " The actual number is usually larger"
                           + " than what is specified here.")
    argParser.add_argument("-b", "--branching", dest="branching", type=int, required=True,
                           help="Approximate avg. branching degree of nodes in this graph.")
    argParser.add_argument("-u", "--upward-edges", dest="upward_edges", action="store_true",
                           help="(Optional) Flag to specify construction of upward edges.")
    args = argParser.parse_args()

    r: int = args.num_roots
    l: int = args.num_leaves
    n: int = args.num_nodes
    b: int = args.branching
    u: bool = args.upward_edges
    dcgGeneration(r, l, b, n, u)
