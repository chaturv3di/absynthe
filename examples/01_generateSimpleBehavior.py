import argparse

from absynthe import TreeBuilder, MonospaceInterleaving


def basicLogGeneration(numRoots: int = 2, numLeaves: int = 4,
                       branching: int = 2, numInnerNodes: int = 16,
                       loggerNodeTypes: str = "SimpleLoggerNode"):
    tree_kwargs = {TreeBuilder.KW_NUM_ROOTS: str(numRoots),
                   TreeBuilder.KW_NUM_LEAVES: str(numLeaves),
                   TreeBuilder.KW_BRANCHING_DEGREE: str(branching),
                   TreeBuilder.KW_NUM_INNER_NODES: str(numInnerNodes),
                   TreeBuilder.KW_SUPPORTED_NODE_TYPES: loggerNodeTypes}

    # Instantiate a concrete GraphBuilder. Note that the
    # generateNewGraph() method of this class returns a
    # new, randomly generated graph that (more or less)
    # satisfies all the parameters provided to the
    # constructor, viz. tree_kwargs in the present case.
    simpleTreeBuilder = TreeBuilder(**tree_kwargs)

    # Instantiate a concrete behavior generator. Some
    # behavior generators do not print unique session ID
    # for each run, but it's nice to have those.
    wSessionID: bool = True
    testBehavior = MonospaceInterleaving(wSessionID)

    # Add multiple graphs to this behavior generator. The
    # behaviors that it will synthesize would essentially
    # be interleavings of simultaneous traversals of all
    # these graphs.
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())
    testBehavior.addGraph(simpleTreeBuilder.generateNewGraph())

    # Specify how many behaviors are to be synthesized,
    # and get going.
    numTraversalsOfEachGraph: int = 2
    for logLine in testBehavior.synthesize(numTraversalsOfEachGraph):
        print(logLine)
    return


if "__main__" == __name__:
    """
    Generates interleaved logs from a few, simple control flow graphs. These graphs are generated
    randomly using command line parameters. The same set of parameters is used to generate all of
    the CFGs.
    """
    argParser = argparse.ArgumentParser(description="Generates interleaved logs from a few, simple"
                                        + " control flow graphs. These graphs are generated"
                                        + " randomly using command line parameters. The same set"
                                        + " of parameters is used to generate all the graphs.")
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
    argParser.add_argument("-t", "--node_types", type=str, required=True,
                           help="Comma separated list of types of logger nodes that can be added"
                           + " to this graph.")
    args = argParser.parse_args()

    r: int = args.num_roots
    l: int = args.num_leaves
    n: int = args.num_nodes
    b: int = args.branching
    t: str = args.node_types
    basicLogGeneration(r, l, b, n, t)
