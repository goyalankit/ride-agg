#!/usr/bin/python
import optparse
import sys
import unittest
import os

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def main(sdk_path, test_path):
    sys.path.insert(0, sdk_path)
    sys.path.insert(0, test_path)
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    if os.environ.get('TRAVIS') == None:
        sys.path.append(os.path.join(os.path.dirname(__file__), './google_appengine'))
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if os.environ.get('TRAVIS') == None:
        SDK_PATH = "/usr/local/google_appengine"
    else:
        SDK_PATH = "./google_appengine"
    TEST_PATH = "./tests"
    main(SDK_PATH, TEST_PATH)
