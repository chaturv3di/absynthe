import unittest

from absynthe.cfg import Node


class NodeTest(unittest.TestCase):

    def test_raisesTypeError(self):
        with self.assertRaises(TypeError):
            _ = Node("AbstractClass? Really?")


if __name__ == '__main__':
    unittest.main()
