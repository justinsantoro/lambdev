import unittest
from lambdev.command_line.run_test import main as run_test


class CommandLineTest(unittest.TestCase):
    def test_run_test(self):
        print(run_test('../lambdev/lambdev_test.yml'))


if __name__ == '__main__':
    unittest.main()