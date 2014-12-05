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
    if sdk_path not in sys.path: sys.path.insert(0, sdk_path)
    if test_path not in sys.path: sys.path.insert(0, test_path)
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    if os.environ.get('TRAVIS') == "true":
        sys.path.append(os.path.join(os.path.dirname(__file__), './google_appengine'))
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(test_path)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if (len(result.errors) > 0):
        exit(1)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()

    SDK_PATH = args[0] if args else "/usr/local/google_appengine"
    TEST_PATH = args[1] if len(args)>1 else "./tests"

    if os.environ.get('TRAVIS'):
        SDK_PATH = "./google_appengine"

    main(SDK_PATH, TEST_PATH)
