import unittest

from absynthe.cfg.logger_node import LoggerNode, SimpleLoggerNode


class LoggerNodeTest(unittest.TestCase):

    def test_abstractClassError(self):
        kwargs = {LoggerNode.key_coreClassName: "UniformNode"}
        with self.assertRaises(TypeError):
            _ = LoggerNode("testLogger", **kwargs)
        return


class SimpleLoggerNodeTest(unittest.TestCase):

    def test_basicTest(self):
        kwargs = {LoggerNode.key_coreClassName: "UniformNode"}
        _ = SimpleLoggerNode("testLogger", **kwargs)
        # _.printDebugInfo()
        return

    def test_logGeneration(self):
        kwargs = {LoggerNode.key_coreClassName: "UniformNode"}
        testLogger = SimpleLoggerNode("testLogger", **kwargs)
        testLogger.printDebugInfo()
        params: list = ["test_param ", "123 ", "more test ", "456.789"]

        # Assert that the same log messages is generated for identical arguments
        self.assertEqual(testLogger.genInfo("11-May-2019, 11:31:13:2323", params),
                         testLogger.genInfo("11-May-2019, 11:31:13:2323", params))

        # Assert that the same error messages is generated for identical arguments
        self.assertEqual(testLogger.genError("11-May-2019, 11:31:13:2323", params),
                         testLogger.genError("11-May-2019, 11:31:13:2323", params))
        return
